from PIL import Image
import numpy as np

def check_lsb(original_path, stego_path, k):
    original_img = Image.open(original_path).convert('L')
    stego_img = Image.open(stego_path).convert('L')
    original_pixels = np.array(original_img).flatten()
    stego_pixels = np.array(stego_img).flatten()
    mask = 2**k - 1
    original_lsb = original_pixels & mask
    stego_lsb = stego_pixels & mask
    diff_lsb = original_lsb != stego_lsb
    num_diff = np.sum(diff_lsb)
    #print(f"Number of pixels with different LSB: {num_diff}")
    #print(f"First few differences (original -> stego):")
    for i in range(min(10, len(original_pixels))):
        if diff_lsb[i]:
            #print(f"Pixel {i}: {original_lsb[i]} -> {stego_lsb[i]}")
    binary_message = ""
    for pixel in stego_pixels:
        lsb_bits = pixel & mask
        binary_message += format(lsb_bits, f'0{k}b')
    end_marker = '11111111'
    if end_marker in binary_message:
        binary_message = binary_message[:binary_message.index(end_marker)]
        #print("Đã tìm thấy dấu kết thúc!")
    else:
        #print("Không tìm thấy dấu kết thúc, trích xuất 128 bit đầu tiên.")
        binary_message = binary_message[:128]
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
    print(f"Thong diep trich xuat duoc: {message}")
    with open("check.txt", "w", encoding="utf-8") as file:
        file.write(message)
    return message

extracted_message = check_lsb("input.png", "output.png", k=2)
