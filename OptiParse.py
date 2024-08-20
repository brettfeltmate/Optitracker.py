from collections.abc import Container

from construct import CString, Float32l, Int16sl, Int32ul, Struct

asset_label = CString('utf8')
packet_asset_count = Int32ul
packet_bytelength = Int32ul
frame_number_prefix = Int32ul
marker_structure = Struct(
    'pos_x' / Float32l,
    'pos_y' / Float32l,
    'pos_z' / Float32l
)
rigid_body_structure = Struct(
    'id' / Int32ul,
    'pos_x' / Float32l,
    'pos_y' / Float32l,
    'pos_z' / Float32l,
    'rot_w' / Float32l,
    'rot_x' / Float32l,
    'rot_y' / Float32l,
    'rot_z' / Float32l,
    'error' / Float32l,
    'valid' / Int16sl,
)


class Parser(object):
    def __init__(self, data: bytes) -> None:
        self.data = memoryview(data)
        self.offset = 0

        self._structs = {
            'label': asset_label,
            'count': packet_asset_count,
            'size': packet_bytelength,
            'prefix': frame_number_prefix,
            'marker': marker_structure,
            'rigid_body': rigid_body_structure,
        }

        self.frame_prefix = self.unpack('prefix')

    def seek_ahead(self, by: int = 0) -> None:
        self.offset += by

    def sizeof(self, asset_type: str, count: int = 1) -> int:
        return self._structs[asset_type].sizeof() * count

    def decode_id(self, encoded_id: int) -> tuple[int, int]:
        tmp_id = Int32ul.parse(encoded_id)
        model_id = tmp_id >> 16
        marker_id = tmp_id & 0x0000FFFF

        return model_id, marker_id

    def unpack(
        self, asset_type: str
    ) -> Container[str | int | float] | int | str:
        struct = self._structs[asset_type]
        unpacked = struct.parse(self.data[self.offset :])
        unpacked.prefix = 

        self.seek_ahead(by=struct.sizeof())

        return unpacked
