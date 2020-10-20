import pysftp

myHostname = "169.56.76.27"
myUsername = "analy"
myPassword = "Kyowon2017!"

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    print ("Connection succesfully stablished ... ")
# Define the file that you want to download from the remote directory
    remoteFilePath = '/data01/logs/analy/maipksap01.allng.com/batch/ir_get_item_parameters_drl.log'
    localFilePath = './test.log'
    sftp.get(remoteFilePath, localFilePath)

sftp.close()