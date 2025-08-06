# CHANGELOG

<!-- version list -->

## v0.22.0 (2025-08-06)

### 🐛 Bug Fixes

- Change open function to importlib.resources.files because other projects can not access the file
  ([`6ac7be9`](https://github.com/adriamontoto/value-object-pattern/commit/6ac7be9288d9312c971fa31765039001dcd73538))

### ✨ Features

- **identifiers**: Implement NussValueObject
  ([`07cbaf8`](https://github.com/adriamontoto/value-object-pattern/commit/07cbaf831053773b62bf0da599c0b669dc14903d))


## v0.21.0 (2025-08-06)

### ✨ Features

- Implement all spain plate value objects
  ([`f992d1f`](https://github.com/adriamontoto/value-object-pattern/commit/f992d1fed3dfe13762c6eaa3ccb6f13821f148e2))


## v0.20.1 (2025-08-05)

### 🐛 Bug Fixes

- Change open function to importlib.resources.files because other projects can not access the file
  ([`008ea32`](https://github.com/adriamontoto/value-object-pattern/commit/008ea32bbee304813fd22eeee8fc33eb53d9a0ce))


## v0.20.0 (2025-08-05)

### ✨ Features

- **plates**: Implement AgriculturalPlateValueObject
  ([`fd08cea`](https://github.com/adriamontoto/value-object-pattern/commit/fd08cea1db3f3e37ce93d80e6b6886ad9f6a727f))

- **plates**: Implement AirForcePlateValueObject
  ([`b5211a2`](https://github.com/adriamontoto/value-object-pattern/commit/b5211a2c4f87a3ee109a2561fab00296ca8e9ba1))

- **plates**: Implement ArmyPlateValueObject
  ([`b65046d`](https://github.com/adriamontoto/value-object-pattern/commit/b65046d1aa923f8edb8393b4e6ae213dfaacecf3))

- **plates**: Implement CarPlateValueObject that supports variations
  ([`02fe0df`](https://github.com/adriamontoto/value-object-pattern/commit/02fe0df32b4fdd83d528cf5582f2d04159ba6089))

- **plates**: Implement CatalanPolicePlateValueObject
  ([`b5a25aa`](https://github.com/adriamontoto/value-object-pattern/commit/b5a25aadcc8871f80112c5677deeafb310bc08e1))

- **plates**: Implement CivilGuardPlateValueObject
  ([`832e619`](https://github.com/adriamontoto/value-object-pattern/commit/832e6198615d6dc093867ec0b065c3d8aab09ee0))

- **plates**: Implement NationalPolicePlateValueObject
  ([`c792d61`](https://github.com/adriamontoto/value-object-pattern/commit/c792d61cfba65c15da6029db8d7e2caf5dd01fab))

- **plates**: Implement NavyPlateValueObject
  ([`7dac40b`](https://github.com/adriamontoto/value-object-pattern/commit/7dac40b03ad9c48cb58bbe35ffa37efc7502dff2))

- **plates**: Implement OrdinaryPlateValueObject
  ([`8a87d66`](https://github.com/adriamontoto/value-object-pattern/commit/8a87d66f0813355824f5de601baa7606caead8ca))


## v0.19.0 (2025-08-05)

### ✨ Features

- **internet**: Implement ImeiValueObject
  ([`81be1c4`](https://github.com/adriamontoto/value-object-pattern/commit/81be1c4ca0c778d9bb734d85fd46c3ece22cc7e7))


## v0.18.0 (2025-08-05)

### ✨ Features

- **identifiers**: Implement PhoneNumberValueObject
  ([`6945733`](https://github.com/adriamontoto/value-object-pattern/commit/694573329c4429b77066776b437d22cffcda3ed7))


## v0.17.0 (2025-08-04)

### ✨ Features

- **internet**: Implement methods for system, user, and ephemeral port ranges in PortValueObject
  ([`e7c4aaf`](https://github.com/adriamontoto/value-object-pattern/commit/e7c4aaf61b5f3d91366dab5dd53477f381a59f6c))


## v0.16.0 (2025-08-04)

### ✨ Features

- **identifiers**: Implement IbanValueObject
  ([`78ef23d`](https://github.com/adriamontoto/value-object-pattern/commit/78ef23d6851186be6933cf93dd5efff415897fc5))


## v0.15.0 (2025-08-04)

### ✨ Features

- **identifiers**: Implement VinValueObject
  ([`1ec705d`](https://github.com/adriamontoto/value-object-pattern/commit/1ec705de43123372daaa799c821b79cbf35814d0))


## v0.14.0 (2025-08-04)

### ✨ Features

- Implement NifValueObject
  ([`95debb5`](https://github.com/adriamontoto/value-object-pattern/commit/95debb5d9ef814b1f25907392a69644c55bd6dc2))

- **identifiers**: Implement Iso3166Alpha2CodeValueObject
  ([`497316c`](https://github.com/adriamontoto/value-object-pattern/commit/497316cfacb15107a90b8f29f8582a1a804a3923))


## v0.13.0 (2025-08-04)

### ✨ Features

- Implement PassportValueObject
  ([`8896bb6`](https://github.com/adriamontoto/value-object-pattern/commit/8896bb69c265be62ddf756b17f80619ff6ea5bfc))


## v0.12.0 (2025-08-04)

### ✨ Features

- Implement NieValueObject
  ([`d02b3ed`](https://github.com/adriamontoto/value-object-pattern/commit/d02b3ed4960da9210fae9ae1da55d956b86405c4))


## v0.11.0 (2025-08-03)

### ✨ Features

- Implement UuidV4ValueObject and StringUuidV4ValueObject
  ([`9699563`](https://github.com/adriamontoto/value-object-pattern/commit/969956397a0e0233b881aa1e8505cf65542305f9))


## v0.10.0 (2025-07-20)

### 🐛 Bug Fixes

- Update string representation methods to use 'self.value' instead of 'self._value'
  ([`66d6489`](https://github.com/adriamontoto/value-object-pattern/commit/66d648972e67096aec108cfb29931164ddc302e2))

### ✨ Features

- Remove unused collection value objects and introduce ListValueObject
  ([`6483727`](https://github.com/adriamontoto/value-object-pattern/commit/64837273f2828142c934a11016cc758b1b920a9f))


## v0.9.3 (2025-07-05)

### 🐛 Bug Fixes

- Check if the provided primitive parameters are constructor BaseModel parameters
  ([`4908540`](https://github.com/adriamontoto/value-object-pattern/commit/490854067782aea88dbf1c207279ecdac3e047ac))


## v0.9.2 (2025-07-05)

### 🐛 Bug Fixes

- Allow BaseModel and ValueObject or their methods to create primitives dictionary
  ([`71bdec5`](https://github.com/adriamontoto/value-object-pattern/commit/71bdec53f3d057e1263d2e8368f8ba6c283aae57))


## v0.9.1 (2025-07-05)

### 🐛 Bug Fixes

- Raise TypeError if BaseModel.from_primitives parameter is not a dictionary of strings
  ([`b28a112`](https://github.com/adriamontoto/value-object-pattern/commit/b28a112535aebfc8c708981f0e0dcb4d95cab293))


## v0.9.0 (2025-07-03)

### ✨ Features

- Ensure enumeration value object can raise custom exceptions
  ([`888e61e`](https://github.com/adriamontoto/value-object-pattern/commit/888e61e4d5601f754429b26076b721962206fb25))


## v0.8.0 (2025-07-03)

### ✨ Features

- Add support for collections value object
  ([`d7e6acd`](https://github.com/adriamontoto/value-object-pattern/commit/d7e6acd53f1b119dcb72543321c6c895dfddf455))


## v0.7.5 (2025-07-02)

### 🐛 Bug Fixes

- When raising enumeration value object errors add enumeration name
  ([`92f087d`](https://github.com/adriamontoto/value-object-pattern/commit/92f087d84c540d0a3f804b4a65f8f71c7048f6f7))


## v0.7.4 (2025-07-02)

### 🐛 Bug Fixes

- Use enum.value when executing to primitives method
  ([`cbf77fe`](https://github.com/adriamontoto/value-object-pattern/commit/cbf77fe54e9b8d3e79d906ad525bd3ee206e24dd))


## v0.7.3 (2025-07-01)

### 🐛 Bug Fixes

- Make enumeration value object to accept the enumeration and enumeration value, not the key
  ([`7975cee`](https://github.com/adriamontoto/value-object-pattern/commit/7975ceecec5e6cfe726dcf9de7879cbd70728ce8))


## v0.7.2 (2025-06-30)

### 🐛 Bug Fixes

- When the primitive value is an enum convert to the enum key
  ([`8b4316f`](https://github.com/adriamontoto/value-object-pattern/commit/8b4316f158e6d015f279ad183187259f199e215a))


## v0.7.1 (2025-06-28)

### 🐛 Bug Fixes

- Fix DniValueObject tests
  ([`392d785`](https://github.com/adriamontoto/value-object-pattern/commit/392d785b6bda3728f7d07489401326a19de80f14))

- Fix equal method tests
  ([`1ee662b`](https://github.com/adriamontoto/value-object-pattern/commit/1ee662b5b194cdd26b3589fe5db77ff71073cc67))


## v0.7.0 (2025-06-28)

### 🐛 Bug Fixes

- Remove bytes string conversion
  ([`8520732`](https://github.com/adriamontoto/value-object-pattern/commit/8520732319ba8e3702312ec8af3d8ec2bf00c091))

### ✨ Features

- Implement base model
  ([`77b6316`](https://github.com/adriamontoto/value-object-pattern/commit/77b6316a8f3eb4d3937a24c96672ef680a86d844))


## v0.6.2 (2025-06-22)

### 🐛 Bug Fixes

- Change the way enumeration type is tested
  ([`9b400cf`](https://github.com/adriamontoto/value-object-pattern/commit/9b400cfc15719e70393eeccbd921daf1e463a8bb))


## v0.6.1 (2025-06-22)

### 📦 Build System

- Bmp object mother pattern package v3.0.0
  ([`ab8ef08`](https://github.com/adriamontoto/value-object-pattern/commit/ab8ef0841bf7c1217bcf827adfa7e0e7126da8ef))


## v0.6.0 (2025-06-21)

### ✨ Features

- Implement none and not none value object
  ([`56df6be`](https://github.com/adriamontoto/value-object-pattern/commit/56df6be41b18b5d5bf79237ab8e0ac30fcd65de2))


## v0.5.0 (2025-06-21)

### ✨ Features

- Implement timezone value object
  ([`0f8cf72`](https://github.com/adriamontoto/value-object-pattern/commit/0f8cf72f096aa681e269854ad65384de0ace2f12))


## v0.4.0 (2025-06-21)

### 🐛 Bug Fixes

- Discard generic warning
  ([`733a126`](https://github.com/adriamontoto/value-object-pattern/commit/733a1262ebdec453862f7f330256eab6e7386ecc))

### ✨ Features

- Implement parameter attribute to change exception text
  ([`93fe71b`](https://github.com/adriamontoto/value-object-pattern/commit/93fe71bb1946ea2b1917f14506d9ad7c27c55fbf))


## v0.3.0 (2025-06-15)

### ✨ Features

- Implement enumeration value object
  ([`cf2b52e`](https://github.com/adriamontoto/value-object-pattern/commit/cf2b52ef9b42efddb9d7c18c27886a1554d339ad))


## v0.2.0 (2025-06-14)

### ✨ Features

- **identifiers**: Implement a function to raise exceptions
  ([`3656cec`](https://github.com/adriamontoto/value-object-pattern/commit/3656cecc1432a494e3629f00308398bdf3a74e6c))

- **primitives**: Implement a function to raise exceptions
  ([`ade1a0b`](https://github.com/adriamontoto/value-object-pattern/commit/ade1a0b151f491b2133f50047a66fe3eb46a873d))


## v0.1.0 (2025-06-13)

### 🐛 Bug Fixes

- Conditionally import 'override' based on Python version
  ([`90cace2`](https://github.com/adriamontoto/value-object-pattern/commit/90cace272f18e31071457c45714dcfa2a8d9e742))

- Correct method call to use instance reference for IPv6 address validation
  ([`f09c464`](https://github.com/adriamontoto/value-object-pattern/commit/f09c4641cfebade033780f6c8b43674b01ff906b))

- Ensure AWS cloud region codes are case-insensitive in validation
  ([`e6407bc`](https://github.com/adriamontoto/value-object-pattern/commit/e6407bc6ad35d7bc990c2c3aa82739b86a1cac23))

- Handle IPv6 address brackets in validation
  ([`6c88275`](https://github.com/adriamontoto/value-object-pattern/commit/6c88275c2fdd4f9c9fd66061b912d32d82550efa))

- Ignore docstring hardcoded secrets
  ([`ba6f172`](https://github.com/adriamontoto/value-object-pattern/commit/ba6f17271382a0ec6e2fd91f3de36b12abb462ec))

- Ignore security warning because there is no risk
  ([`bc1b358`](https://github.com/adriamontoto/value-object-pattern/commit/bc1b358314f17edc6d3251be4d23e9edb87a747c))

- Move get top layer domains outside DomainValueObject so there is no data leaking
  ([`2575744`](https://github.com/adriamontoto/value-object-pattern/commit/2575744b7f0324dcf98cd2ffab6f78f3b58497f2))

- Remove unused imports
  ([`df92952`](https://github.com/adriamontoto/value-object-pattern/commit/df9295270aa18f56e273f05fb135467afad106f9))

- Update aws cloud region value object regions url
  ([`7a7998a`](https://github.com/adriamontoto/value-object-pattern/commit/7a7998a9f655e8ad4a13d95ada2049e5836f7c26))

- Update import for override based on Python version
  ([`b0f11b8`](https://github.com/adriamontoto/value-object-pattern/commit/b0f11b8fcd953da73906713426289581ab6d28a1))

- Valueobject validation and process were not following the designed order
  ([`ae66553`](https://github.com/adriamontoto/value-object-pattern/commit/ae665532136cc8abba33b2548cee9ab46e3bef2b))

### 📦 Build System

- Remove requirements file and add dependencies to pyproject
  ([`34d37cb`](https://github.com/adriamontoto/value-object-pattern/commit/34d37cbf2380f9791f306fbbe761083e69d568ab))

- Remove tests from builded package
  ([`2043eee`](https://github.com/adriamontoto/value-object-pattern/commit/2043eee4589e03540b0d25356d08d9f3c870015d))

- Update object-mother-pattern version to 2025.1.12 in dependencies
  ([`88ba639`](https://github.com/adriamontoto/value-object-pattern/commit/88ba639128a9e65c0dca2104353cc13f43c27bdc))

### ✨ Features

- Enhance validation decorators with order handling
  ([`f799710`](https://github.com/adriamontoto/value-object-pattern/commit/f799710d79db6172895440588e67d9ae71e1cfa6))

- First commit
  ([`61f3057`](https://github.com/adriamontoto/value-object-pattern/commit/61f3057a3ed59fef7501f6735d1e2ff17a4fd818))

- Implement AwsCloudRegionValueObject for AWS region validation
  ([`46dd9fe`](https://github.com/adriamontoto/value-object-pattern/commit/46dd9fe1c2a6f6b30efde8ba5efd51bf843a2bee))

- Implement Base16, Base32, Base56, Base58, and Base64 value objects for string validation
  ([`40a15d3`](https://github.com/adriamontoto/value-object-pattern/commit/40a15d38d0cc10d7d2c2b7650187dbf67bdea893))

- Implement DateValueObject and DatetimeValueObject for date management
  ([`688a6d5`](https://github.com/adriamontoto/value-object-pattern/commit/688a6d5595cf46dffbbb5395b56e54ad58122ab8))

- Implement DniValueObject for validating Spanish DNI format
  ([`f41c857`](https://github.com/adriamontoto/value-object-pattern/commit/f41c85771e795a466767ea86a7461d779cf1d17c))

- Implement DomainValueObject for domain name validation
  ([`6bb940c`](https://github.com/adriamontoto/value-object-pattern/commit/6bb940cb2d0ef901ddf016108bc9e38780e9024e))

- Implement HexadecimalStringValueObject for validating hexadecimal strings
  ([`3ba70d5`](https://github.com/adriamontoto/value-object-pattern/commit/3ba70d5a2f7c2e8255b3d3fb06d737d09314e519))

- Implement HostValueObject for host validation
  ([`26f4923`](https://github.com/adriamontoto/value-object-pattern/commit/26f49232b6810e3102867d325baf021d94c716fb))

- Implement HttpUrlValueObject, HttpsUrlValueObject, and HttpHttpsUrlValueObject for enhanced URL
  validation
  ([`7375c1f`](https://github.com/adriamontoto/value-object-pattern/commit/7375c1fe8ce69cc88d212890a1b30cd4872d77b7))

- Implement Ipv4AddressValueObject for managing IPv4 addresses
  ([`11b6674`](https://github.com/adriamontoto/value-object-pattern/commit/11b66740c6f3ec1ebf5939fba8f176712d2010b1))

- Implement Ipv4NetworkValueObject for managing IPv4 networks
  ([`c2ec2d3`](https://github.com/adriamontoto/value-object-pattern/commit/c2ec2d35e1e5aea12d9cebbb366e5ec84092cd40))

- Implement Ipv6AddressValueObject for managing IPv6 addresses
  ([`3a256c4`](https://github.com/adriamontoto/value-object-pattern/commit/3a256c4b272abc00382d995421ff6e2d4d6910f9))

- Implement Ipv6NetworkValueObject for managing IPv6 networks
  ([`6f9a73c`](https://github.com/adriamontoto/value-object-pattern/commit/6f9a73ce6d851a97f76c7c3377c96d3de179739b))

- Implement MacAddressValueObject for managing MAC addresses
  ([`f10fc2a`](https://github.com/adriamontoto/value-object-pattern/commit/f10fc2ace39ef955d4a3ffd3329e3648a13a07cc))

- Implement PortValueObject for managing network port
  ([`f036725`](https://github.com/adriamontoto/value-object-pattern/commit/f03672587464f4db07ec8c19b08fca4a20f26891))

- Implement post-validation processing to ValueObject
  ([`02315ae`](https://github.com/adriamontoto/value-object-pattern/commit/02315aecdd0313887587a28a98b9d415a6c4c99d))

- Implement process decorator and refactor value object processing methods
  ([`ceaadee`](https://github.com/adriamontoto/value-object-pattern/commit/ceaadeead02375775ed74d74b6466fa2a36c0440))

- Implement StringUuidValueObject and UuidValueObject for UUID management
  ([`67e13a8`](https://github.com/adriamontoto/value-object-pattern/commit/67e13a89d297a9ea5d41443fd0ce0fb3b7403ed5))

- Implement title attribute in value object model
  ([`b335943`](https://github.com/adriamontoto/value-object-pattern/commit/b33594303997c2f4283296a0f7f8887a66cbb13a))

- Implement unit tests for value object eq, hash, str, repr methods
  ([`e9b4f94`](https://github.com/adriamontoto/value-object-pattern/commit/e9b4f944637a15eb79055ae9f32aa11428645864))

- Implement UrlValueObject for URL handling and validation
  ([`ad6a7d9`](https://github.com/adriamontoto/value-object-pattern/commit/ad6a7d9e89fbb7d7e84d8d6588169989a37d7fa8))

- Implement usage examples to value object classes
  ([`8cdd307`](https://github.com/adriamontoto/value-object-pattern/commit/8cdd3074df5378d1e053a4ae2ab2fab85812da31))

- Implement validation decorator and refactor value object validation methods
  ([`5501b47`](https://github.com/adriamontoto/value-object-pattern/commit/5501b47e946cde87967abb6cb3e91b67674e1004))

- Implement validation method in value object class
  ([`976b022`](https://github.com/adriamontoto/value-object-pattern/commit/976b0226acfbb95632c262e430cecfd724caca64))

- Implement value object implementations for primitive types (string, bytes, boolean, float,
  integer)
  ([`104714e`](https://github.com/adriamontoto/value-object-pattern/commit/104714e0d457e3d455d661fc15115b5118cd8e35))

- Implement value object simple class and its unit tests
  ([`64ba018`](https://github.com/adriamontoto/value-object-pattern/commit/64ba018627dba67a34ce89f2bb8869cf02bae7d9))

- Implement value objects for AWS, resend, openai and github
  ([`7448881`](https://github.com/adriamontoto/value-object-pattern/commit/7448881645cadfdc3a401268164529b215eef78e))

- Remove unused value objects and its tests
  ([`4d90b80`](https://github.com/adriamontoto/value-object-pattern/commit/4d90b8008879f8c929e492b7ede480f2e7cc4581))
