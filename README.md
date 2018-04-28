# CloneDir
CloneDir is an incremental file/folder backup engine built using Python. CloneDir was originally developed to backup audio files from household devices to a centralised Raspberry Pi media hub.

CloneDir uses hash-based file verfication mechanisms to detect block changes and can synchronise changes from multiple devices in real-time. 

## CloneDir Architecture
This repository implements CloneDir Engine and Client both of which are stored in seperate folders.

#### 1. CloneDir Engine
CloneDir Engine is the main CloneDir daemon that runs on a backup device such as a Raspberry Pi connected to a hard-drive. It can receive backup, update and restore requests from multiple CloneDir clients. 

To start the CloneDir Engine use:
```
python3 engine.py
```

#### 2. CloneDir Client
CloneDir Client is the client scipt that is used on an end device to connect and synchronise data with the CloneDir Engine.

To run the CloneDir Client use the following command on a directory you want to perform the action:
```
python3 client.py MODE
```

** Available Modes **
1. -add - Add this directory for backup. This is run for the first time when a directory is initialised as a backup directory.
2. -sync - Synchronise changes in this directory. This is run on an existing backed up directory.
3. -restore - Restore an existing backed up directory.
