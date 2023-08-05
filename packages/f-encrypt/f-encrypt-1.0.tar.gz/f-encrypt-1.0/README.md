# f-encrypt
Simple tool to encrypt and decrypt files

## Usage

```bash
# Option 1: enter your key with an option
f-encrypt <file> --key <key>

# Option 2: enter your key using an env var
export F_ENCRYPT_KEY=<key>
f-encrypt <file>

# Option 3: Prompt for password
f-encrypt <file>
Enter Key: <key>

# Decrypting uses the same --key and env-var setup
f-decrypt <file>
```

To replace the file instead of printing its encrypted/decrypted contents, set `F_ENCRYPT_REPLACE`
to `true`. Note that this can be somewhat dangerous - if something goes wrong you could lose your
file.

```bash
export F_ENCRYPT_REPLACE=true
```


---


## Installation

### From source

```bash
virtualenv --python=python3 env/
source env/bin/activate
pip install .
```
