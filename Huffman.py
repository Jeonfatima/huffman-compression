import os
import heapq  #to check isinstance condition



class PQNode:
        def __init__(self,char,freq):
                self.char = char
                self.freq = freq
                self.left = None
                self.right = None
        def __lt__(self,others):  #(__ for private func) and lt means less than
                return self.freq< others.freq  #return ture agar hamari di hui node ki freq ziyada hai
        def __eq__(self,others): #eq = equal
            if (others == None):
                    return False
            if(not isinstance(others, PQNode)):
                    return False
            return self.freq == others.freq
        
class HuffmanCoding:
    def __init__(self,path):
        self.path = path #path of file to be compressed
        self.pQ=[]
        self.codes={} #to store converted huffman coded
        self.reverse_mapping = {} #do reverse mapping from code value to the charachter mapping


                   
    def make_frequency_dict(self,text):
        """calc freq of each character and return"""
        frequency = {}
        for ch in text:
            if not ch in frequency:
                frequency[ch] = 0
            frequency[ch] += 1 #increase count if character present
        return frequency
    
    def make_pQ(self,frequency):#make_heap is make priorty queue
        """make prioirty queue"""
        for key in frequency:
            node = PQNode(key, frequency[key])
            heapq.heappush(self.pQ,node)


    
    def merge_codes(self):#build huffman tree and save root node in heap(PQ)
        while(len(self.pQ)>1):
            node1 = heapq.heappop(self.pQ)
            node2 = heapq.heappop(self.pQ)

            merged = PQNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.pQ, merged)

    def make_codes_helper(self, node, current_code):
        if(node == None):
            return
        
        if(node.char != None):
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char #here it stores mapping from code to character

        self.make_codes_helper(node.left, current_code + "0")            
        self.make_codes_helper(node.right, current_code + "1") 

    def make_codes(self):#make codes for characters and save
        root = heapq.heappop(self.pQ)
        current_code = ""
        self.make_codes_helper(root,  current_code)

    def get_encoded_text(self,text): #replace character with code and return
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text 

    def pad_encoded_text(self,encoded_text):# make  encoded text 8 bits long if needed and return
        extra_padding = 8 - len(encoded_text) % 8 #
        for i in range(extra_padding): # adds 0 jitna ki zaoorat hai 
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding) #coverts into 8 bits binary format
        encoded_text = padded_info + encoded_text #merge kar raha hai
        return encoded_text 


    def get_byte_array(self,padded_encoded_text): # converting bits into bytes (8 bits = 1 byte)
        b = bytearray() # b is byte array
        for i in range(0,len(padded_encoded_text),8): 
            byte = padded_encoded_text[i:i+8]  # i mai 8 + kar raha hai..
            b.append(int(byte,2)) #2 is base of binary
        return b

    def compress(self):
        filename,file_extension = os.path.splitext(self.path)
        output_path= filename + ".bin"
        
        with open(self.path,'r') as file,open(output_path,'wb')as output: #open inputfile in readmode and open outputfile in write in binary mode
            text = file.read()
            text = text.rstrip()

            frequency =  self.make_frequency_dict(text)
            self.make_pQ(frequency)
            self.merge_codes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text) #stores byte array
            output.write(bytes(b)) #writing in file named output

        print("Compressed")
        return output_path
    

    # --------decompression-------
    def remove_padding(self,bit_string):#remove padding and return
         padded_info = bit_string[:8]#read padding info which is presented start of encoded text in 8 bit stream(as string)
         extra_padding = int(padded_info, 2) # we will get the int value like how many bits are added

         bit_string = bit_string[8:]#remove padded info from our string
         encoded_text = bit_string[:-1*extra_padding] #remove the padded bits to get actual encodded code#using substring with neg[-1] value to remove those padded bits from the end


         return encoded_text
    
    def decode_text(self, encoded_text):  # decode and return
       current_code = ""  # temporary var
       decoded_text = ""  # string of decoded text which will return

    #make sure reverse_mapping is not empty
       if not self.reverse_mapping:
           print("Error: reverse_mapping is empty. Make sure the same object is used for decompression.")
           return ""

       for bit in encoded_text:  # read 1 bit at a time from string of encoded text
        current_code += bit  # keep on adding in our current code

        if current_code in self.reverse_mapping:  # if current code is present in reverse_mapping that means it will be a valid huffman code
            character = self.reverse_mapping[current_code]
            decoded_text += character  # append the recieved character into output decode 
            current_code = ""  # reinitialize the current code into empty string to start reading for next stream of bits 

       # warn if any leftover bits not decoded
        if current_code != "":
         print("Warning: leftover bits found — file might be corrupted or padding not removed properly.")

        return decoded_text



    def decompress(self,input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompress" + ".txt"
        
        with open(input_path,'rb') as file ,open(output_path,'w') as output:
            bit_string =""

            byte = file.read(1)# reads 1 byte from a file
            while (len(byte) > 0): #gives empty value when reaches end of file
                byte = ord(byte) #byte ko int mai convert (A to 65)
                bits = bin(byte)[2:].rjust(8,'0') # converts int to binary ...(65 -> 0b100001)...[2:] removes 0b...rjust(8,'0')making sure its 8 bit long by adding 0
                bit_string += bits
                byte = file.read(1) #reads next byte 
             
            encoded_text = self.remove_padding(bit_string)
            decoded_text = self.decode_text(encoded_text)

            output.write(decoded_text)
        
        print("Decompressed")
        return output_path#return the output path where our decompressed file is saved
      












