from flask import Flask,request,jsonify
import os
from cipher.rsa import RSACipher
import shutil
app=Flask(__name__)

rsa_cipher=RSACipher()
@app.route("/api/rsa/generate_keys", methods=["POST"])
def generate_keys():
    data = request.json
    sender_name = data.get("sender_name")
    sender_name_2 = data.get("sender_name_2")
    if sender_name or sender_name_2:
        # Handle the case when either sender_name or sender_name_2 is provided
        if sender_name_2:
            folder_path = f'sender_name/{sender_name_2}'
            public_key, private_key,p,q = rsa_cipher.generate_keys()
            
            public_key_path = f'{folder_path}/{sender_name_2}_public.txt'
            private_key_path = f'{folder_path}/{sender_name_2}_private.txt'

            sender_name_2_p_path=f'{folder_path}/{sender_name_2}_p.txt'
            sender_name_2_q_path=f'{folder_path}/{sender_name_2}_q.txt'
            directory = os.path.dirname(public_key_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            if not os.path.exists(public_key_path):
                with open(public_key_path, "w") as f:
                    f.write(str(public_key))

                with open(private_key_path, "w") as f:
                    f.write(str(private_key))
                with open(sender_name_2_p_path,"w") as f:
                    f.write(str(p))
                with open(sender_name_2_q_path,"w") as f:
                    f.write(str(q))
                global receiver_pub_key,receiver_pr_key,receiver_p,receiver_q
                receiver_pub_key,receiver_pr_key,receiver_p,receiver_q=rsa_cipher.load_keys(folder_path)
                return jsonify({"message": f"Keys Generated Successfully for {sender_name_2}"})
            else:
                return jsonify({"message": f"Your keys have already been generated for {sender_name_2}"})

        if sender_name:
            folder_path = f'sender_name/{sender_name}'
            
            public_key,private_key,p,q=rsa_cipher.generate_keys()
            public_key_path = f'{folder_path}/{sender_name}_public.txt'
            private_key_path = f'{folder_path}/{sender_name}_private.txt'
            sender_name_p_path = f'{folder_path}/{sender_name}_p.txt'
            sender_name_q_path = f'{folder_path}/{sender_name}_q.txt'
            directory = os.path.dirname(public_key_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            if not os.path.exists(public_key_path) :
                with open(public_key_path, "w") as f:
                    f.write(str(public_key))

                with open(private_key_path, "w") as f:
                    f.write(str(private_key))
                with open(sender_name_p_path,"w") as f:
                    f.write(str(p))
                with open(sender_name_q_path,"w") as f:
                    f.write(str(q))
                
                global pub_inst_2,pr_key,p_inst_2,q_inst_2
                pub_inst_2,pr_key,p_inst_2,q_inst_2=rsa_cipher.load_keys(folder_path)
                return jsonify({"message": f"Keys Generated Successfully for {sender_name}"})
            else:
                return jsonify({"message": f"Your keys have already been generated for {sender_name}"})
    else:
        return jsonify({"message": "You need to input your name(s) to generate keys"})


@app.route("/api/rsa/encrypt",methods=["POST"])
def encrypt_and_send_package():
    data=request.json
    sender=data.get("sender")
    receiver=data.get("receiver")
    package=data.get("package")
    if sender and receiver and package:
        folder_path=f'sender_name/{sender}'
        receiver_key_path=f'sender_name/{receiver}'
        receiver_path=f'{receiver_key_path}'
        if os.path.exists(folder_path):
            if os.path.exists(receiver_path):
                if package and os.path.isfile(package):
                    sender_destination_path = os.path.join(folder_path, os.path.basename(package))
                    shutil.copy2(package, sender_destination_path)
                    
                    if os.path.isfile(sender_destination_path):
                        with open(sender_destination_path, "rb") as f:
                            file_bytes = f.read()
                        try:
                            content_str = file_bytes.decode('utf-8')
                            cipher=rsa_cipher.encrypt(content_str,receiver_pub_key)
                            encrypted_path = os.path.join(folder_path, 'encrypted_package.txt')
                            with open(encrypted_path, "wb") as f:
                                f.write(cipher)
                            shutil.copy2(encrypted_path,receiver_path)
                            os.remove(encrypted_path)
                            os.remove(sender_destination_path)
                            return jsonify({"message":f"File Encrypted and sent to {receiver} successfully"})
                        except UnicodeDecodeError:
                            return jsonify({"message":"File type incompatible to be encrypted"})
                else:
                    return jsonify({"message":"You need to upload a file to start encryption"}) 
            else:
                return jsonify({"message":"This receiver doesn't exist"})
        else:   
            return jsonify({"message":"This sender doesn't exist"})       
    elif (sender and package) or (receiver and package):
        if not sender:
            return jsonify({"message":"You need to enter the name of the sender"})
        elif not receiver:
            return jsonify({"message":"You need to enter the name of the receiver"})
    else:
        return jsonify({"message":"You need to enter the name of the sender and the receiver in order to proceed with encrypt"})
    
@app.route("/api/rsa/decrypt",methods=["POST"])
def find_and_decrypt_file():
    data=request.json
    receiver=data.get("receiver")
    file_name="encrypted_package.txt"
    receiver_folder=f'sender_name/{receiver}'
    
    intended_file=os.path.join(receiver_folder,file_name)
    #file_open=open(intended_file,"rb")
    #load_encrypted_content=pickle.load(file_open)
    #file_open.close()
    with open(intended_file,"rb") as f:
        bytes=f.read()
        decrypted_text=rsa_cipher.decrypt(bytes,receiver_pr_key)
    os.remove(intended_file)
    return jsonify({"message":"Decrypted Successfully","decrypted":f'{decrypted_text}'})

@app.route("/api/rsa/sign",methods=["POST"])
def sign_package():
    data=request.json
    suggester=data.get("sender")
    receiver_1=data.get("receiver")
    package_1=data.get("package")
    if suggester and receiver_1:
        if suggester:
          suggester_1_folder_path=f'sender_name/{suggester}'
          receiver_prepare_path=f'sender_name/{receiver_1}'
          if os.path.exists(suggester_1_folder_path):
            with open(package_1,"rb") as f:
                file_bytes=f.read()
                try:
                    content_str=file_bytes.decode('utf-8')
                    signature=rsa_cipher.sign(content_str,pr_key)
                    signature_hex=signature.hex()
                    signed_file=os.path.join(suggester_1_folder_path,"signed_file.txt")
                    with open(signed_file,"w") as f:
                        f.write(signature_hex)
                    shutil.copy2(signed_file,receiver_prepare_path)
                    shutil.copy2(package_1,receiver_prepare_path)
                    os.remove(signed_file)
                    return jsonify({"message":f"File signed and sent successfully to {receiver_1}"})
                except UnicodeDecodeError:
                    return jsonify({"message":"Invalid file type to sign"})  
          else:
              return jsonify({"message":"This sender doesn't exist"})
        
        
        if receiver_1:
            suggester_2_folder_path=f'sender_name/{receiver_1}'
            if os.path.exists(suggester_2_folder_path):# your list of filenames
                if os.path.isfile(package_1):
                    receiver_folder_path=os.path.join(suggester_2_folder_path,os.path.basename(package_1))
                    #shutil.copy2(package_1,receiver_folder_path) 
                return jsonify({"message":f"Signed file and orginal file sent successfully to {receiver_1}"})
            else:
                return jsonify({"message":"This receiver doesn't exist"})
    


@app.route("/api/rsa/verify",methods=["POST"])
def verify_integrity():
    data=request.json
    suggester=data.get("sender")
    receiver=data.get("receiver")
    package_1=data.get("package")
    if suggester and receiver:
        if receiver:
            folder_path=f'sender_name/{receiver}'
            target_file="signed_file.txt"
            target_file_path= os.path.join(folder_path,target_file)
            orginal_file=os.path.basename(package_1)
            orginal_file_receiver_path=os.path.join(folder_path,orginal_file)
            with open(orginal_file_receiver_path,"rb") as f:
                file_bytes=f.read()
            try:
                content_str=file_bytes.decode("utf-8")
                with open(target_file_path,"rb") as f:
                    signature_bytes=f.read()
                    signature_bytes_str=signature_bytes.decode("utf-8")
                    signature=bytes.fromhex(signature_bytes_str)
                legit_result=rsa_cipher.verify(content_str,signature,pub_inst_2)
            except UnicodeDecodeError:
                return 
            if legit_result:
                return jsonify({"message":f"This signature is {legit_result} and belongs to {suggester}"}) 
            else:
                return jsonify({"message":f"This signature is {legit_result} and doesn't belong to {suggester}"})
            
            
            
            
            
          
          
            
            




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    
    