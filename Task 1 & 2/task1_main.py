import tkinter as tk
import hashlib
import key_pairs
from key_pairs import stored_key_pairs as keys

#signing the record function
def sign(record, inv_name):
    #hashing the record
    #convert the record to bytes so the hashing works
    record_bytes = record.encode('utf-8')
    #display it for the calculations
    bytes_var.set(record_bytes)    

    #hash the record + converted to hexadecimal string 
    hashed_record = hashlib.sha256(record_bytes).hexdigest()
    #display it for the calculations
    hash_var.set(hashed_record)
    
    #s = m^d mod n
    #convert hex to decimal for mathing
    m = int(hashed_record, 16)
    
    #display it for the calculations
    dec_var.set(m)
    
    #retrieve the inventories private key pair
    private_key_pair = keys['inv_'+inv_name+'_priv_key']
    #retrieve n and d from the keypair
    n = private_key_pair['n']
    d = private_key_pair['d']
    s = pow(m, d, n)
    
    #display it for the calculations
    sig_var.set(s)
    return s
    
#compare the decrypted signature to the original message
def verify_sig(s, inv_name, record):
    #m’ = s^e mod n 
    public_key_pair = keys['inv_'+inv_name+'_pub_key']
    e = public_key_pair['e']
    n = public_key_pair['n']
    dec_sig = pow(s, e, n)
    decsig_var.set(dec_sig)
    
    #hash the record 
    hashed_record = hashlib.sha256(record.encode('utf-8')).hexdigest()
    
    #convert hashed record to decimal like when encrypting it 
    decimal_hash = int(hashed_record, 16)
    
    #Displaying it in the working out 
    original_msg_hashed_val.set(decimal_hash)
    
    #make the decrypted sig back to decimal back to hash 
    if (dec_sig == decimal_hash):
        valid_var.set('yes')
    else :
        valid_var.set('no')
   
#submit button function
def submit():
    #record entered 
    record = record_var.get()
    
    #Logic: get the last character from the string and check which inventory it is, then sign the message
    length = len(record)
    signature = ''
    char = record[length - 1]
    if char == 'A' or char == 'B' or char == 'C' or char == 'D':
        #sign using their private key 
        signature= sign(record, char.lower())
        display_calcs(char.lower())
        verify_sig(signature, char.lower(), record)
    else:
        error_var.set("INVENTORY DOES NOT EXIST")
        #clear all other fields 
        p_var.set('')
        q_var.set('')
        e_var.set('')
        n_var.set('')
        d_var.set('')
        phin_var.set('')
        bytes_var.set('')
        hash_var.set('')
        dec_var.set('')
        sig_var.set('')
        decsig_var.set('')
        valid_var.set('')
        original_msg_hashed_val.set('')
        
    
# UI 

#create a widget (named m for master)
m= tk.Tk()

#create tk variable for the entered record 
record_var = tk.StringVar()

#vars for storing answers for display
p_var = tk.StringVar()
q_var = tk.StringVar()
e_var = tk.StringVar()
n_var = tk.StringVar()
d_var = tk.StringVar()
phin_var = tk.StringVar()
bytes_var = tk.StringVar()
hash_var = tk.StringVar()
dec_var  = tk.StringVar()
sig_var = tk.StringVar()
decsig_var = tk.StringVar()
valid_var = tk.StringVar()
original_msg_hashed_val = tk.StringVar()
error_var = tk.StringVar()


def display_calcs(inv_name):
    # TRY FIND A CLEANER WAY 
    if (inv_name == 'a'):
        p_var.set(key_pairs.inv_a_p)
        q_var.set(key_pairs.inv_a_q)
        e_var.set(key_pairs.inv_a_e)
        n_var.set(key_pairs.inv_a_n)
        d_var.set(key_pairs.inv_a_d)
        phin_var.set(key_pairs.inv_a_phin)
    elif (inv_name == 'b'):
        p_var.set(key_pairs.inv_b_p)
        q_var.set(key_pairs.inv_b_q)
        e_var.set(key_pairs.inv_b_e)
        n_var.set(key_pairs.inv_b_n)
        d_var.set(key_pairs.inv_b_d)
        phin_var.set(key_pairs.inv_b_phin)
    
    elif (inv_name == 'c'):
        p_var.set(key_pairs.inv_c_p)
        q_var.set(key_pairs.inv_c_q)
        e_var.set(key_pairs.inv_c_e)
        n_var.set(key_pairs.inv_c_n)
        d_var.set(key_pairs.inv_c_d)
        phin_var.set(key_pairs.inv_c_phin)
    
    elif (inv_name == 'd'):
        p_var.set(key_pairs.inv_d_p)
        q_var.set(key_pairs.inv_d_q)
        e_var.set(key_pairs.inv_d_e)
        n_var.set(key_pairs.inv_d_n)
        d_var.set(key_pairs.inv_d_d)
        phin_var.set(key_pairs.inv_d_phin)
        
#Prompt to enter a record:
tk.Label(m, text='Enter a new record').grid(row=0)
#inputbox
e1 = tk.Entry(m, textvariable = record_var).grid(row=0, column= 1)
error = tk.Label(m, textvariable = error_var).grid(row=0, column= 2)
#e1.grid(row=0, column= 1)

#submit button
entBtn = tk.Button(m, text='Enter', command = submit).grid(row=2, column= 0)
#entBtn.grid(row=2, column= 0)

#lables to display all the calcs
tk.Label(m, text= 'Calculations for RSA signing:').grid(row=3, column = 0)
tk.Label(m, text= 'Variables:').grid(row=4, column = 0)
tk.Label(m, text= 'p= ').grid(row=5, column = 0)
tk.Label(m, textvariable = p_var).grid(row=5, column = 1)

tk.Label(m, text= 'q= ').grid(row=6, column = 0)
tk.Label(m, textvariable = q_var).grid(row=6, column = 1)

tk.Label(m, text= 'e= ').grid(row=7, column = 0)
tk.Label(m, textvariable = e_var).grid(row=7, column = 1)


tk.Label(m, text= 'Public key calculations (n, e):').grid(row=8, column = 0)
tk.Label(m, text= 'n [p*q]= ').grid(row=9, column = 0)
tk.Label(m, textvariable = n_var).grid(row=9, column = 1)

tk.Label(m, text= 'e= ').grid(row=10, column = 0)
tk.Label(m, text = '[repeated]').grid(row=10, column = 1)


tk.Label(m, text= 'Private key calculations (n, d):').grid(row=11, column = 0)
tk.Label(m, text= 'n [p*q]= ').grid(row=12, column = 0)
tk.Label(m, text= '[repeated]').grid(row=12, column = 1)

tk.Label(m, text= 'phi(n) [q-1]*[p-1]= ').grid(row=13, column = 0)
tk.Label(m, textvariable = phin_var).grid(row=13, column = 1)

tk.Label(m, text= 'd [e^-1 mod phi(n)]= ').grid(row=14, column = 0)
tk.Label(m, textvariable = d_var).grid(row=14, column = 1)


tk.Label(m, text= 'Signing Process').grid(row=15, column = 0)
tk.Label(m, text= 'Convert record to bytes: ').grid(row=16, column = 0)
tk.Label(m, textvariable = bytes_var).grid(row=16, column = 1)

tk.Label(m, text= 'Hash record: ').grid(row=17, column = 0)
tk.Label(m, textvariable = hash_var).grid(row=17, column = 1)

tk.Label(m, text= 'Convert to decimal: ').grid(row=18, column = 0)
tk.Label(m, textvariable = dec_var).grid(row=18, column = 1)

tk.Label(m, text= 'Sign message using private key (s = m^d mod n): ').grid(row=19, column = 0)
tk.Label(m, textvariable = sig_var).grid(row=19, column = 1)

tk.Label(m, text= 'Validating the signature using public key (n,e)').grid(row=20, column = 0)

tk.Label(m, text= 'Original message:').grid(row=21, column = 0)
tk.Label(m, textvariable = original_msg_hashed_val).grid(row=21, column = 1)

tk.Label(m, text= 'Decrypted signature:').grid(row=22, column = 0)
tk.Label(m, textvariable = decsig_var).grid(row=22, column = 1)

tk.Label(m, text= 'Valid?:').grid(row=23, column = 0)
tk.Label(m, textvariable = valid_var).grid(row=23, column = 1)


m.mainloop()
