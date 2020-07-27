Q: *retrying failed action with response code: 403 ({"type"=>"cluster_block_exception", "reason"=>"blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];"})*
A: 
  1. *read_only_allow_delete*
  ```yaml
  PUT _all/_settings 
  {"index.blocks.read_only_allow_delete": null}
  ```
  2. *disk storage*
  ```yaml
  PUT _cluster/settings
  {
    "transient": {
      "cluster.routing.allocation.disk.watermark.low": "10gb",
      "cluster.routing.allocation.disk.watermark.high": "5gb",
      "cluster.routing.allocation.disk.watermark.flood_stage": "1gb",
      "cluster.info.update.interval": "1m"
    }
  }
  ```
