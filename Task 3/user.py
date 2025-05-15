# # procurement officer
# No idea where to use this
proc_off_p = 1080954735722463992988394149602856332100628417
proc_off_q = 1158106283320086444890911863299879973542293243
proc_off_e = 106506253943651610547613

#validation stuff for later 
# def pkg_encrypt_message(s):
#     #compute individual
#     result = pow(s, pkg_e, pkg_n)
#     return result

# def pkg_encrypt_second(m, t):
#     #get the each servers id 
#     A_id = inv_A_key_req()
#     B_id = inv_B_key_req()
#     C_id = inv_C_key_req()
#     D_id = inv_D_key_req()
    
#     #append message to t
#     m = str(t) + str(m)
#     #hash message
#     hash_m = hashlib.md5(m.encode()).hexdigest()
#     #convert message to int 
#     decimal_m = int(hash_m, 16)

#     new_t = pow(int(t), decimal_m, pkg_n)
#     result_2 = A_id * B_id * C_id * D_id * new_t % pkg_n
#     return result_2