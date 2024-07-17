from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from hashlib import sha256
import os
import pickle
import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce

    def compute_hash(self):
        block_string = "{}{}{}{}{}".format(
            self.index, self.previous_hash, self.transactions, self.timestamp, self.nonce
        )
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.chain[-1] if self.chain else None
        new_block = Block(
            index=(last_block.index + 1 if last_block else 0),
            previous_hash=(last_block.compute_hash() if last_block else "0"),
            transactions=self.unconfirmed_transactions,
            timestamp=time.time(),
        )

        proof = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        return proof

    def proof_of_work(self, block, difficulty=2):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def save_object(self, obj, filename):
        with open(filename, "wb") as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

main = Tk()
main.title("Blockchain Based Certificate Validation")
main.geometry("1300x1200")

blockchain = Blockchain()

if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)

def save_certificate():
    global filename
    text.delete('1.0', END)

    filename = askopenfilename(initialdir="certificate_templates")
    with open(filename, "rb") as f:
        bytes_data = f.read()

    roll_no = tf1.get()
    name = tf2.get()
    contact = tf3.get()

    if roll_no and name and contact:
        digital_signature = sha256(bytes_data).hexdigest()
        data = f"{roll_no}#{name}#{contact}#{digital_signature}"
        blockchain.add_new_transaction(data)
        _hash = blockchain.mine()
        b = blockchain.chain[-1]

        text.insert(END, f"Blockchain Previous Hash: {b.previous_hash}\n")
        text.insert(END, f"Block No: {b.index}\n")
        text.insert(END, f"Current Hash: {b.hash}\n")
        text.insert(END, f"Certificate Digital Signature: {digital_signature}\n\n")

        blockchain.save_object(blockchain, 'blockchain_contract.txt')
    else:
        text.insert(END, "Please enter Roll No")

def verify_certificate():
    text.delete('1.0', END)

    filename = askopenfilename(initialdir="certificate_templates")
    with open(filename, "rb") as f:
        bytes_data = f.read()

    digital_signature = sha256(bytes_data).hexdigest()
    flag = True

    for i in range(1, len(blockchain.chain)):
        b = blockchain.chain[i]
        data = b.transactions[0]
        arr = data.split("#")

        if arr[3] == digital_signature:
            text.insert(END, "Uploaded Certificate Validation Successful\n")
            text.insert(END, "Details extracted from Blockchain after Validation\n\n")
            text.insert(END, f"Roll No: {arr[0]}\n")
            text.insert(END, f"Student Name: {arr[1]}\n")
            text.insert(END, f"Contact No: {arr[2]}\n")
            text.insert(END, f"Digital Sign: {arr[3]}\n")
            flag = False
            break

    if flag:
        text.insert(END, "Verification failed or certificate modified")

font = ('times', 15, 'bold')
title = Label(main, text='Blockchain Based Certificate Validation')
title.config(bg='bisque', fg='purple1')
title.config(font=font)
title.config(height=3, width=120)
title.place(x=0, y=5)

font1 = ('times', 13, 'bold')
l1 = Label(main, text='Roll No:')
l1.config(font=font1)
l1.place(x=50, y=100)
tf1 = Entry(main, width=20)
tf1.config(font=font1)
tf1.place(x=180, y=100)

l2 = Label(main, text='Student Name:')
l2.config(font=font1)
l2.place(x=50, y=150)
tf2 = Entry(main, width=20)
tf2.config(font=font1)
tf2.place(x=180, y=150)

l3 = Label(main, text='Contact No:')
l3.config(font=font1)
l3.place(x=50, y=200)
tf3 = Entry(main, width=20)
tf3.config(font=font1)
tf3.place(x=180, y=200)

save_button = Button(main, text="Save Certificate with Digital Signature", command=save_certificate)
save_button.place(x=50, y=250)
save_button.config(font=font1)

verify_button = Button(main, text="Verify Certificate", command=verify_certificate)
verify_button.place(x=420, y=250)
verify_button.config(font=font1)

text = Text(main, height=15, width=120)
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10, y=300)
text.config(font=font1)

main.config(bg='cornflower blue')
main.mainloop()
