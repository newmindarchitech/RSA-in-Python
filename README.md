# Python RSA
This repository is a personal Python project that has fully implemented the functionalities of the RSA algorithm with a basic front-end UI for interaction. The features I have implemented in the RSA algorithm were:
- Encryption
- Decryption
- Sign
- Verify






The purpose of this repository is the display of my understanding of the RSA algorithm and how I have implemented RSA algorithm in Python
## Set up
In order to clone and run this project into your machine. Here are some commands you need to do

At the root of the project, first run this command 


```
pip install -r requirements.txt 
```


Alternatively, you can run this command using the latest version of Python that includes pip as part of the installation

```
python -m pip install -r requirements.txt
```


After installing the essential libraries for this project has been done. You need to run these two files





``` python rsa_interface.py (for the UI of the application) ``` 




``` python api.py (for the gateways the UI calls to for each button)```

### Limitations
Although this project works, there are some limitations you need to be aware of:

- One-sided functionality between the sender and the receiver. Meaning the sender(at the left) can only encrypt and send the encrypted file to the receiver(at the right) and not vice-versa despite what the UI implies
- Keys are only loaded after generating keys for the sender and receiver. Meaning that the functionalities of the RSA algorithm only works while the application is active


