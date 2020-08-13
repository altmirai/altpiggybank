# AltPiggyBank
(version 0.0.x)

***ALTPIGYBANK IS PRE-ALPHA SOFTWARE. USE AT YOUR OWN RISK.***

***READ RISKS AND WARNINGS BELOW BEFORE USING ALTPIGGYBANK.***

***see www.altmirai.com for more information on cryptoasset custody and for tutorials on how to perform secure cryptoasset safekeeping.***

___
___
# Description
AltPiggyBank is an open-sourced command line tool that provides the functionality required to turn cloud HSM services into a simple, affordable, and highly secure Bitcoin wallet.

___
___

# Installation

    pip install altpiggybank



___
___

# Usage 

___



### Create a Bitcoin Address:
<br/>

**STEP 1:** Generate a ECC Key Pair using the secp256k1 curve in  **your cloud HSM**.

*Example (using AWS CloudHSM):*

    Command:  genECCKeyPair -i 16 -l test1

    Cfm3GenerateKeyPair returned: 0x00 : HSM Return: SUCCESS
    Cfm3GenerateKeyPair:    public key handle: 3670038    private key handle: 3670074
    Cluster Error Status
    Node id 15 and err state 0x00000000 : HSM Return: SUCCESS
*Take note of the ECC Key Pair's public key (**VK**) handle and private key (**SK**) handle.*

<br/>

**STEP 2:** Export public key in a PEM format file from **your cloud HSM**.

*Example (using AWS CloudHSM):*

    Command:  exportPubKey -k 3670038 -out pubKey3670038.pem

    PEM formatted public key is written to pubKey3670038.pem
    Cfm3ExportPubKey returned: 0x00 : HSM Return: SUCCESS

<br/>

**STEP 3:** Convert PEM file to Bitcoin Address

**piggy addr** [ *pem file* ] [ **-v** *public key handle* ] [ **-s** *private key handle* ]

    $ piggy addr --help
    Usage: piggy addr [OPTIONS] PEM_FILE

    Options:
        -v TEXT  Your cloud HSM's public key(VK) handle  [required]
        -s TEXT  Your cloud HSM's private key(SK) handle  [required]
        --help   Show this message and exit.

*Example:*

    $ piggy addr pubKey3670038.pem -v 3670038 -s 36700740

    File addr3670038.json created
    File 3670038.csv created

    Address: 17oMUEB53gQDSEHyVL9FLZobEL8FnsRvR1
    Confirmed Balance(SAT): 0 as of 18:21:09 08/10/20

*The CSV file can be imported into a spreadsheet for record keeping.*
*The addr JSON file is what altpiggybank will use to generate a transaction to transfer Bitcoin out of your address.*
*altpiggybank calls an api from sochain.com for confirmed balance data.*

<br/>

___

### Refresh a Bitcoin Address

<br/>

**piggy refresh** [ *addr JSON file* ]

    piggy refresh --help
    Usage: piggy refresh [OPTIONS] ADDR_JSON_FILE

    Options:
      --help  Show this message and exit.

*Example:*

    $ piggy refresh addr2621938.json

    File 2621938.csv created

    Address: 1BHznNt5x9rqMQ1dpWy4fw5y5PSJV3ZR3L
    Confirmed Balance(SAT): 5659056 as of 18:52:27 08/10/20

<br/>

___

### Transaction Fee Estimate

<br/>

**piggy fee** [ *addr JSON file* ] [ **-a** *send all btc* ] [ **-p** *send partial btc* ]

    piggy fee --help
    Usage: piggy fee [OPTIONS] ADDR_JSON_FILE

    Options:
        -p      Send some of BTC in address to recipient's address and balance to
                change address

        -a      Send all BTC in address to recipient's address NOTE: This argument
                is mutually exclusive with partial  [required]

    --help  Show this message and exit.
   
*Example:*

    $ piggy fee addr2621938.json -a

    The fee estimates for a transaction for 1BHznNt5x9rqMQ1dpWy4fw5y5PSJV3ZR3L with 1 inputs and 1 outputs are:

    Fastest: 41472 sat
    Half hour: 41472 sat
    One hour: 36096 sat

*altpiggybank calls an api from Bitcoinfees.earn.com for fee recommendations.*

<br/>

---

### Create an Unsigned Transaction

<br/>

**piggy tx** [ *addr JSON file* ][ **-a** *send all btc* ] [ **-p** *send partial btc* ] [ **-f** *mining fee in SATs* ] [ **-r** *recipient address* ] [ **-q** *quantity of BTC to transfer in SATs* ] [ **-c** *change address* ]


    $ piggy tx --help
    Usage: piggy tx [OPTIONS] ADDR_JSON_FILE


    Options:
        -a          Send all BTC in address to recipient's address NOTE: This
                    argument is mutually exclusive with partial  [required]

        -p          Send some of BTC in address to recipient's address and balance
                    to change address

        -f INTEGER  mining fee  [required]
        -r TEXT     The address you are sending BTC to  [required]
        -q INTEGER  The ammount of BTC being sent to recipient's address in SATs
                    NOTE: This argument is mutually exclusive with all  [required]

        -c TEXT     Change address NOTE: This argument is mutually exclusive with
                    all  [required]

        --help      Show this message and exit.

*Example:*

    altpiggybank % piggy tx addr2621938.json -a -f 30000 -r 17oMUEB53gQDSEHyVL9FLZobEL8FnsRvR1

    File unsignedTx2621938_1.bin created
    File tx2621938.json created

***altpiggybank will create one unsignedTx file for each transaction input.***

*The above example only contains one input, but you may be required to sign and upload multiple tx files.*
*altpiggybank calls an api from sochain.com for transaction input data.*

---

### Sign a Transaction

<br/>

**STEP 1:** Sign the unsignedTx file with your private key stored in **your cloud HSM**.

*Example (using AWS CloudHSM):*

    Command:  sign -f unsignedTx2621938_1.bin -k 2621448 -m 17 -out signedTx2621938_1.der

    Signature creation successful
    signature is written to file signedTx2621938_1.der
    Cfm3Sign: sign returned: 0x00 : HSM Return: SUCCESS

**STEP 2** Verify your signature with your public key in **your cloud HSM**.

*Example (using AWS CloudHSM):*

    Command:  verify -f unsignedTx2621938_1.bin -s signedTx2621938_1.der -k 2621938 -m 17

    Signature verifition successful
    Cfm3Verify returned: 0x00 : HSM Return: SUCCESS

**STEP 3** Add signature(s) to your transaction.

**piggy signed** [ *tx json file* ] [ **-sig** *signedTx file* ]


    $ piggy signed tx2621938.json -sig signedTx2621938_1.der 

    Copy and past the below raw transaction into a third-party broadcast transaction service.

    010000000150a0ebe15416c79d4ae5d8628d2e1bfa9046e9cde26d9e3943a398783eea9af3000000008a47304402206e772678740907038d1b08b059291955c74f07ec3c104fbc89f781238bd7223402205a96a974f3ad330315d546c93bb81c1cd714ed2cd636e678a4cdd3cc5238f139014104101ff6444366dd092f95a5f4829c3bf6ae0311e86b8b37d5184a3430211c79232765d0870bbcef4ab510754d1e1cd7f0f60975a5c227380fc68529ad80406ee2ffffffff0180e45500000000001976a9144a94f9d8ffc48b899300a3d2ceb76b0e342009da88ac00000000


<br/>

___

# Broadcast a Transaction

<br/>

Altpiggybank does not currently support transaction broadcasting. Several free online services exist where a user can copy and paste the above transaction hex to broadcast a transactions.

<br />

___
___

# Risks

Private keys generated and stored in a cloud HSM services are better protected against theft or loss than with other non-custodial Bitcoin storage. You, however, have an active role in that security.

You must keep access to your cloud account secure. Cloud providers have extensive identity access management (IAM) tools and resources to help users secure thier accounts. Learn and follow best IAM pratices.

Private keys are not the only attack vector used to steal Bitcoin. An attacker can alter transaction data and trick you into unwittingly sending them your bitcoin. The data at risk, includes: (1) Your address prior to recieving Bitcoin, (2) The recipient's address, (3) Your change address, and (4) Unsigned transactions. Verify this data before any transaction.

---
___
xs
# Warnings

Version 0.0.1 of AltPiggyBank:

- Is not secure. An attacker can alter its code to provide false data.

- May contain bugs that impact your ability to access your Bitcoin.

- Is designed as a proof of concept only, not as production code.

The authors of AltPiggyBank assume no liability for the correctness of the code or any of the contents of the packages. Use AltPiggyBank at your own risk.



  



