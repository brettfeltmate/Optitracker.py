from collections.abc import Container

from construct import CString, Float32l, Int16sl, Int32ul, Struct

asset_name = CString('utf8')
num_assets = Int32ul
packet_length = Int32ul
frame_number = Int32ul

marker_structure = Struct(
    'pos_x' / Float32l, 'pos_y' / Float32l, 'pos_z' / Float32l
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
        self.stream_position = 0

        self._structs = {
            'label': asset_name,
            'count': num_assets,
            'size': packet_length,
            'prefix': frame_number,
            'marker': marker_structure,
            'rigid_body': rigid_body_structure,
        }

        self.frame_prefix = self.unpack('prefix')

    def seek_ahead(self, skip: int = 0) -> None:
        self.stream_position += skip

    def sizeof(self, asset_type: str, count: int = 1) -> int:
        return self._structs[asset_type].sizeof() * count

    def decode_id(self, encoded_id: bytes) -> tuple[int, int]:
        tmp_id = Int32ul.parse(encoded_id)
        model_id = tmp_id >> 16
        marker_id = tmp_id & 0x0000FFFF

        return model_id, marker_id

    def unpack(
        self, asset_type: str
    ) -> Container[str | int | float] | int | str:
        struct = self._structs[asset_type]
        unpacked = struct.parse(self.data[self.stream_position :])

        self.seek_ahead(skip=struct.sizeof())

        return unpacked
