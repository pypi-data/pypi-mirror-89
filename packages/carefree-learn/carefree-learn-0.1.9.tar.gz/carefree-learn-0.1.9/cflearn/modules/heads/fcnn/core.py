import torch

from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Optional

from ..base import HeadBase
from ...blocks import MLP


@HeadBase.register("fcnn")
class FCNNHead(HeadBase):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        hidden_units: List[int],
        mapping_configs: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        final_mapping_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(in_dim, out_dim)
        if mapping_configs is None:
            mapping_configs = {}
        self.mlp = MLP(
            in_dim,
            out_dim,
            hidden_units,
            mapping_configs,
            final_mapping_config=final_mapping_config,
        )

    def forward(self, net: torch.Tensor) -> torch.Tensor:
        return self.mlp(net)


__all__ = ["FCNNHead"]
