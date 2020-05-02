| action | time | 
| :--- | :--- |
| describe promql parser ast | 2020.05.02 |


---

---

```golang
// Node is a generic interface for all nodes in an AST
//
// Whenever numerous nodes are listed such as in a switch-case statement
// or a chain of function definitions (e.g. String(), expr(), etc.) convention is
// to list them as follows:
//
// 	- Statements (语句)
// 	- statement types (alphabetical)
// 	- ...
// 	- Expressions
// 	- expression types (alphabetical)
// 	- ...
//
```
- **Node interface**

    ```golang
    type Node interface {
        // String representation of the node that returns the given node when parsed
        // as part of a valid query.
        // 作为有效查询的一部分,解析时返回给定节点的节点的字符串表示形式

        String() string

        // PositionRange returns the position of the AST Node in the query string.
        // PositionRange 返回AST节点在查询字符串中的位置。
        PositionRange() PositionRange
    }
    ```

- **Statement interface**

    ```golang
    // Statement is a generic interface for all statements.
    type Statement interface {
        Node

        // stmt ensures that no other type accidentally implements the interface
        // 确保没有其他类型的接口意外实现
        // nolint:unused
        stmt()
    }
    ```

- **Expr interface**

    ```golang
    // Expr is a generic interface for all expression types.
    type Expr interface {
        Node

        // Type returns the type the expression evaluates to. It does not perform
        // in-depth checks as this is done at parsing-time.
        // 返回表达式求值的类型。它不执行深入检查，因为这是在解析时完成的
        Type() ValueType
        // expr ensures that no other types accidentally implement the interface.
        // if equal to stmt() interface
        expr()
    }
    // Expressions is a list of expression nodes that implements Node.
    type Expressions []Expr
    ```

- **EvalStmt**

    ```golang
    // EvalStmt holds an expression and information on the range it should
    // be evaluated on.
    // EvalStmt 定义 一个表达式和有关应该对其求值的范围的信息
    type EvalStmt struct {
        Expr Expr // Expression to be evaluated.

        // The time boundaries for the evaluation. If Start equals End an instant
        // is evaluated.
        Start, End time.Time
        // Time between two evaluated instants for the range [Start:End].
        // expr : (end - start)
        Interval time.Duration
    }

    func (*EvalStmt) stmt() {}
    ```

- **AggregateExpr**

    ```golang
    // AggregateExpr represents an aggregation operation on a Vector.
    // AggregateExpr 对 矢量对象的聚合操作
    type AggregateExpr struct {
        Op       ItemType // The used aggregation operation. -> Operators,Aggregators,Keywords
        Expr     Expr     // The Vector expression over which is aggregated.
        Param    Expr     // Parameter used by some aggregators. -> 在聚合过程中使用的参数
        Grouping []string // The labels by which to group the Vector. -> 分组的标签
        Without  bool     // Whether to drop the given labels rather than keep them. -> 是否删除labels
        PosRange PositionRange
    }
    ```

- **BinaryExpr**

```golang
// BinaryExpr represents a binary expression between two child expressions.
type BinaryExpr struct {
	Op       ItemType // The operation of the expression.
	LHS, RHS Expr     // The operands on the respective sides of the operator. -> 两侧的操作数

	// The matching behavior for the operation if both operands are Vectors.
    // If they are not this field is nil.
    // 如果两个操作数都是向量，则操作的匹配行为。如果不是，则此字段为nil。
	VectorMatching *VectorMatching

	// If a comparison operator, return 0/1 rather than filtering.
	ReturnBool bool
}
```

- **Call**

    ```golang
    // Call represents a function call.
    type Call struct {
        Func *Function   // The function that was called.
        Args Expressions // Arguments used in the call.

        PosRange PositionRange
    }
    ```

- **MatrixSelector**

    ```golang
    // MatrixSelector represents a Matrix selection.
    // MatrixSelector 定义矩阵
    type MatrixSelector struct {
        // It is safe to assume that this is an VectorSelector
        // if the parser hasn't returned an error.
        // 如果解析器没有返回错误,这是一个VectorSelector
        VectorSelector Expr
        Range          time.Duration

        EndPos Pos
    }
    ```

- **SubqueryExpr**

    ```golang
    // SubqueryExpr represents a subquery.
    type SubqueryExpr struct {
        Expr   Expr
        Range  time.Duration
        Offset time.Duration
        Step   time.Duration

        EndPos Pos
    }
    ```

- **NumberLiteral**

    ```golang
    // NumberLiteral represents a number.
    type NumberLiteral struct {
        Val float64

        PosRange PositionRange
    }
    ```

- **ParenExpr**

    ```golang
    // ParenExpr wraps an expression so it cannot be disassembled as a consequence
    // of operator precedence.
    // ParenExpr 包装了一个表达式，因此它不能由于运算符优先级而被反汇编
    type ParenExpr struct {
        Expr     Expr
        PosRange PositionRange
    }
    ```

- **StringLiteral**

    ```golang
    // StringLiteral represents a string.
    type StringLiteral struct {
        Val      string
        PosRange PositionRange
    }
    ```

- **UnaryExpr**

    ```golang
    // UnaryExpr represents a unary operation on another expression.
    // Currently unary operations are only supported for Scalars.
    // 对另一个表达式的一元运算 (Scalars)
    type UnaryExpr struct {
        Op   ItemType
        Expr Expr

        StartPos Pos
    }
    ```

- **VectorSelector**

    ```golang
    // VectorSelector represents a Vector selection.
    type VectorSelector struct {
        Name          string
        Offset        time.Duration
        LabelMatchers []*labels.Matcher

        // The unexpanded seriesSet populated at query preparation time.
        UnexpandedSeriesSet storage.SeriesSet
        Series              []storage.Series

        PosRange PositionRange
    }

    ```