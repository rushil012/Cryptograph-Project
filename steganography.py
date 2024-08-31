#  programming 
# author: Rushil Nagpal
# date: 5/20/2023
'''
file: Cryptography is a program that encrypts and decrpts messages given by the user. Different techniques
are implemented such as least significant bit technique, caeser cipher python, huffman codes
'''
# input: Inputs that are given by the user are message to encrypt, the files to encode/decode
# output: Output the message, bytes, binary coding


# steganography
#importing all the necessary files for steganography project
import cv2
import types
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher
class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    #Function that encodes the message given from one file to the other file
    #New file gets created if the file does not exist and the message gets written into that file
    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein) #Reading the input image using OpenCV-Python
        #print(image) # for debugging, add a few print statements if needed
        
        # calculate available byte
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)
        # convert into binary
        if codec == 'binary':
            self.codec = Codec()
            binary = self.codec.encode(message+self.delimiter)
            num_bytes = ceil(len(binary)//8) + 1 
            if  num_bytes > max_bytes:
                print("Error: Insufficient bytes!")
            else:
                print("Bytes to encode:", num_bytes) 
                self.text = message
                self.binary = binary

            index = 0

            data_len = len(self.binary) #Finding the length of the data that needs to be hidden
            for values in image:
                for pixel in values:
                    #convert RGB values to binary format
                    r, g, b = self.codec.encode(pixel)
                    #modify the least significant bit if there is still data to store
                    if index < data_len:
                        pixel[0] = int(r[:-1] + self.binary[index], 2) #This is for red
                        index += 1
                    if index < data_len:
                        pixel[1] = int(g[:-1] + self.binary[index], 2) #This is for green
                        index += 1
                    if index < data_len:
                        pixel[2] = int(b[:-1] + self.binary[index], 2) #This is for blue
                        index += 1
                    if index >= data_len:
                        break
        
            cv2.imwrite(fileout,image) #outputing the text into a new file


        elif codec == 'caesar':
            self.codec = CaesarCypher()
            image = cv2.imread(filein) #reads the file
            max_bytes = image.shape[0] * image.shape[1] * 3 // 8
            print("Maximum bytes available:", max_bytes)
            binary = self.codec.encode(message+self.delimiter)
            num_bytes = ceil(len(binary)//8) + 1 
            if  num_bytes > max_bytes:
                print("Error: Insufficient bytes!")
            else:
                print("Bytes to encode:", num_bytes) 
                self.text = message
                self.binary = binary
                # your code goes here
                # you may create an additional method that modifies the image array
                shape = image.shape #finds the shape of the image
                n = image.flatten() #flattens the image
                binary2 = ""
                for i in n:
                    binary2 += bin(i)
                    if binary2[-1] == 1:
                        binary2[-1] += 1
                    elif binary2[-1] == 0:
                        binary2[-1] -=1
                image = np.reshape(n, shape)
                cv2.imwrite(fileout, image)
        #elif codec == 'huffman':
            #self.codec = HuffmanCodes()

    #Message gets decoded from the given output file and original message gets printed          
    def decode(self, filein, codec):
        image = cv2.imread(filein)
       
        if codec == 'binary':
            self.codec = Codec()
            binary_data = ""
            for values in image:
                for pixel in values:
                    r, g, b = self.codec.encode(pixel) #convert the red,green and blue values into binary format
                    binary_data += r[-1] #this is for red
                    binary_data += g[-1] #this is for green
                    binary_data += b[-1] #this is for blue
            all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-1:] == "#":
                    break
            self.text = (decoded_data[:-1])

        elif codec == 'caesar':
            self.codec = CaesarCypher()
            image = cv2.imread(filein)

            y = image.flatten()
            binary2 = ""
            elements = []
            for i in y:
                binary2 += bin((i))
                elements.append(binary2[-1])
            binary_data = self.codec.encode(self.text+self.delimiter)
            # update the data attributes:
            print(binary_data)
            self.text = self.codec.decode(binary_data)
            print(self.text)
            self.binary = self.codec.encode(self.text+self.delimiter)
            
            
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        
    #prints messsage and the binary version of it    
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary) 
    #Shows the images of both the stegno images
    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()
    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    s.decode('fractal.png', 'binary')
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
