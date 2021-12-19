# Solution to day 16 of AOC 2021, Packet Decoder
# https://adventofcode.com/2021/day/16

def slicer(s: str, slice_pos: int) -> tuple:
    """Return a tuple of strings which are the parm string cleaved at its parm slice position."""
    return s[0:slice_pos], s[slice_pos:]


def decode(bits: str) -> str:
    global VERSION_SUM

    print()
    print('parsing new packets')
    print('bits:', bits)

    # Every packet begins with a standard header: the first three bits encode the packet version.
    packet_version_raw, bits = slicer(bits, 3)
    packet_version = int(packet_version_raw, 2)
    print('packet_version:', packet_version)
    VERSION_SUM += packet_version

    # ... and the next three bits encode the packet type ID.
    packet_type_id_raw, bits = slicer(bits, 3)
    packet_type_id = int(packet_type_id_raw, 2)
    print('packet_type_id:', packet_type_id)

    # Packets with type ID 4 represent a literal value.
    if packet_type_id == 4:
        print('parsing a literal')
        literal_value_raw = ''
        continue_ind = '1'
        while continue_ind == '1':
            five_bits, bits = slicer(bits, 5)
            continue_ind, num_bits_raw = slicer(five_bits, 1)
            literal_value_raw += num_bits_raw

        print('  literal_value_raw:', literal_value_raw)
        literal_value = int(literal_value_raw, 2)
        print('  literal_value:', literal_value)

        # # The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.
        # _, bits = slicer(bits, 3)

    # Every other type of packet (any packet with a type ID other than 4) represent an operator...
    else:
        length_type_id, bits = slicer(bits, 1)

        # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the
        # sub-packets contained by this packet.
        if length_type_id == '0':
            sub_packet_length_raw, bits = slicer(bits, 15)
            sub_packet_length = int(sub_packet_length_raw, 2)
            print('sub_packet_length:', sub_packet_length)

            sub_packet, bits = slicer(bits, sub_packet_length)
            print('sub_packet:', sub_packet)
            while len(sub_packet) > 0:
                sub_packet = decode(sub_packet)

        # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets
        # immediately contained by this packet.
        else:
            assert length_type_id == '1'
            num_of_sub_packets_raw, bits = slicer(bits, 11)
            num_of_sub_packets = int(num_of_sub_packets_raw, 2)
            print('num_of_sub_packets:', num_of_sub_packets)

            for sub_packet_iterations in range(num_of_sub_packets):
                bits = decode(bits)

    return bits


def decode_hex(h: str) -> str:
    h_to_b = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
              '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}

    start_bits = ''
    for digit in h:
        start_bits += h_to_b[digit]

    return decode(start_bits)


assert slicer(s='123456789', slice_pos=2) == ('12', '3456789')

VERSION_SUM = 0
decode_hex('8A004A801A8002F478')
assert VERSION_SUM == 16

VERSION_SUM = 0
decode_hex('620080001611562C8802118E34')
assert VERSION_SUM == 12

VERSION_SUM = 0
decode_hex('C0015000016115A2E0802F182340')
assert VERSION_SUM == 23

VERSION_SUM = 0
decode_hex('A0016C880162017C3686B18A3D4780')
assert VERSION_SUM == 31

f = open('input.txt')
hex_str = f.read()
f.close()

print('hex:', hex_str)
VERSION_SUM = 0
left_over_bits = decode_hex(hex_str)
print('left_over_bits', left_over_bits)
print('VERSION_SUM:', VERSION_SUM)
