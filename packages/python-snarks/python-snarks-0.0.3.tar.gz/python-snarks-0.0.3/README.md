# python-snarks

This is a Python implementation of zkSNARK schemes. This library is based on [snarkjs](https://github.com/iden3/snarkjs), and uses the output from [circom](https://github.com/iden3/circom).

For now, it is for research purpose, not implemented for product.

# Install
```
$ pip install python-snarks
```

# Usage

```python
import os
from python_snarks import Groth, Calculator, gen_proof, is_valid

def test_groth():
    ## 1. setup zkp
    print("1. setting up...")
    gr = Groth(os.path.dirname(os.path.realpath(__file__)) + "/circuit/circuit.r1cs")
    gr.setup_zk()

    ## 2. proving
    print("2. proving...")
    wasm_path = os.path.dirname(os.path.realpath(__file__)) + "/circuit/circuit.wasm"
    c = Calculator(wasm_path)
    witness = c.calculate({"a": 33, "b": 34})
    proof, publicSignals = gen_proof(gr.setup["vk_proof"], witness)
    print("#"*80)
    print(proof)
    print("#"*80)
    print(publicSignals)
    print("#"*80)

    ## 3. verifying
    print("3. verifying...")
    result = is_valid(gr.setup["vk_verifier"], proof, publicSignals)
    print(result)
    assert result == True
```

### export solidity verifier

Groth class's export_solidity_verifier function creates solidity file. You can deploy it on ethereum network and use it as a verifier.

```python
import os
from python_snarks import Groth, Calculator, gen_proof, is_valid

def test_groth():
    ## 1. setup zkp
    print("1. setting up...")
    gr = Groth(os.path.dirname(os.path.realpath(__file__)) + "/circuit/circuit.r1cs")
    gr.setup_zk()
    gr.export_solidity_verifier("verifier.sol")
```

### verifying on contract

```python
result = contract_instance.functions.verifyProof(
        ...proof and public signals...
    ).call()
```

# Test

```
$ pytest tests/test_groth16.py
```

# Supported platforms

The supported platforms currently support are set to the requirements of the [wasmer-python](https://github.com/wasmerio/wasmer-python).

# TODO

* Compatibility with the latest snarkjs, circom
* Performance optimizing
