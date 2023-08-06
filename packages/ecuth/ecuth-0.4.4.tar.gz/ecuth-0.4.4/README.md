# ECUTH

A library for authentication and authorization with public key signature, using random challenge/response.

The main motivation for writing this package was to be able to use an established HTTP authentication scheme with Metamask to sign a challenge to prove identity. However, the package is (hopefully) designed to work in any generic case.

The server application in `/example` demonstrates the Metamask use-case, at the same time demonstrating all parts of the package.


## Usage

In the `examples` folder a `uwsgi` HTTP server is provided. This illustrates how to use the `eip712` and `hoba` filters to perform a pure HTTP authentication using Metamask as a signer, using the `EthereumRetriever` implementation.

To run the server, you need the "uwsgi python plugin" installed. Once you have, you can run it like this:

`uwsgi --wsgi-file examples/server.py --http :5555`

(note that the provided config uses port 5555 in the origin. It has no special meaning, just made up on the spot. If you change it, you will have to change the config, too).

The recipe is as follows:

1. Server generates and stores the challenge, and sends it to the client in a `WWW-Authentication` header along with `realm` and `max-age`.
2. Client uses the challenge to generate the HOBA signature material.
3. Client hashes the HOBA signature material with sha256.
4. Client uses the _hashed_ HOBA signature material as the challenge in the EIP712 schema.
5. Client serializes the challenge according to the EIP712 schema.
6. Client prompts the puny human to sign the serialized data in step 5 above with Metamask.
7. Client generates the HOBA authorization header value and sends it to the server. Note that:
	* the challenge part of the header is the original server challenge.
	* the signature part is a signature on the HOBA-challenge-wrapped-in-EIP712 described in steps 2-6 above.
8. Server parses the header, verifies that the challenge hasn't expired.
9. Server retrieves the filter pipeline from the stored challenge and executes it on the original challenge. The filters are, in sequence:
	* HOBA filter
	* SHA256 filter (this filter is defined in the server example source file directly)
	* EIP712 filter
10. The resulting value of step 9 is the data signed by the client. The ethereum address of the client is recovered using the signature and this data.
11. Server requests a file at the base-url with filename matching the 0x-hex of the recovered ethereum address.
12. If the file can be retrieved and is readable, it means that the authentication was a success. There should be much rejoicing.


## Overview

### ACL

The ACL items used in this example constitute a simple key/value store, implemented with the `YAMLAcl` class. The document must:

* be a valid YML document.
* must have two top-level elements; `level` and `items`.
* `items` must be a collection of key/value entries on a single-level.
* the value of each `item` must be `0` (no access), `2` (write) or `4` (read). (any key with value 0 can optionally be omitted).

```
level: <level>
items:
  foo: 0
  foo.bar: 2
  xyzzy.baz: 4
  ...
```


#### Interpretation

The `level` field defines an hierarchical criteria for changing data:

> If `level` of user `X` is _lower_  or _equal to_ `level` of user `Y`, then user `X`  **cannot** _change_ or _delete_ data for that user.

The values for the `items` keys are a simplificaiton of the `chmod` bitflag used in unix systems;

* If `0x04` is set, read access is granted.
* If `0x02` is set, write access is granted.


#### GNUPG ACL encryption

The example uses gnupg for encryption of the ACL list.

Provided in this repository is a `.gnupg` resource directory with the keys used in the test and server, along with the `test/data` directory containing:

* exported keys
* the ACL source file
* the encrypted and signed ACL source file
* The private key (and keystore file) of the ethereum key used in the example

The latter was generated with this command:

`gpg -aer 245508630E91CA06EFA1FBB20B297F3839D18362 --sign -u 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 -o test/data/0xe1AB8145F7E55DC933d51a18c793F901A3A0b276 test/data/data.yml`

The test/server gnupg setup will expect the key that _signed_ the ACL document to be _fully trusted_. The trustdb in `.gnupg` already includes this trust. Of course I'm not gonna give you my secret key, so you may want to try yourself with your own. When you do, just remember you have to update the trust settings.

... or just write your own decrypter method, dang nabbit :)


### Filters

A deterministic transformation pipeline of the challenge can be added by using filter methods. This is useful in cases where the client needs to wrap the data before signing it.

Two filters are provided in the `ecuth.filters` package:

* **EIP712**: Metadata wrapper for Ethereum, increasingly standard in the ecosystem, and soon-to-be enforced by the Metamask message signer.
* **HOBA**: The HTTP Origin-Bound Authentication scheme, which allows authentication with client signing a challenge using public key crypto, exactly what we're exploring here.

These filters each have additional dependencies, defined as `extra_requires` in the `setup.cfg` file (i.e. to install them both, use `pip install ecuth[eip712,hoba])`


#### EIP712

Described in [https://eips.ethereum.org/EIPS/eip-712](https://eips.ethereum.org/EIPS/eip-712)

The provided filter will expect the challenge to be provided wrapped in the following (pseudo) schema:

```
const challenge_type = [
	{
	type: 'bytes',
	name: 'challenge',
	}
];

const domain_type = [
	{ 
		name: "name",
		type: "string"
	},
	{
		name: "version",
		ype: "string"
	},
	{
		name: "chainId",
		type: "uint256",
	},
//{ name: "verifyingContract", type: "address" },
//{ name: "salt", type: "bytes32" },
];

const data_to_serialize_and_sign = {
	types: {
		EIP712Domain: domain_type,
		Challenge: challenge_type,
	},
	primaryType: "Challenge",
	domain: <domain_data>,
	message: {
		challenge: <challenge_value>,
	},
}	
```

(`verifyingContract` and `salt` are commented out as the contract part not yet implemented)

To be clear; this schema is custom designed for the EIP712 filter and example server (see below).


#### HOBA

A superficial study of the existing authentication schemes for HTTP has suggested that HOBA is the least "hacky" for the purposes of a simple challenge/response mechanism where the public key is known to the server. The only caveat is that the `secp256k1` signature algorithm used with Ethereum (and other cryptocurrencies) is not standardized as an IANA public key signature algo scheme. In fact, at the time of writing, only `RSA-SHA256` and `RSA-SHA1` are. Since all numbres between 2 and 99 are up for grabs, the arbitrary but not quite unpretentious number `42` has been chosen in the dependency package `http-hoba-auth` written specifically to support this package. So, collisions may happen. Beware.

That being said; it's anyway advisable to read [RFC 7486](https://tools.ietf.org/html/rfc7486) before you use this filter.
