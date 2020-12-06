pragma solidity ^0.4.24;

contract P2P_Video {
    string ipfs_video_hash = "";
    string ipfs_signature_hash = "";
    string ipfs_public_key_hash = "";
    
    address public owner = 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4;
    address public buyer = 0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2;
    
    uint price = 0;
    string description = "";
    
    uint stage = 0;
    
    enum State { AWAITING_PAYMENT, AWAITING_DELIVERY, COMPLETE }
    
    State private currState;
    
    modifier onlyBuyer() {
        require(msg.sender == buyer, "Only buyer can call this method");
        _;
    }
    
    function getStore() public view returns (string, string, string, uint, string) {
        if (currState == State.COMPLETE) {
            return (ipfs_video_hash, ipfs_signature_hash, ipfs_public_key_hash, price, description);
        }
        
    }
    
    function setStore(string _ipfs_video_hash, string _ipfs_signature_hash, string _ipfs_public_key_hash, uint _price, string _description) public {
        require(msg.sender == owner, "Only buyer can call this method");

        ipfs_video_hash = _ipfs_video_hash;
        ipfs_signature_hash = _ipfs_signature_hash;
        ipfs_public_key_hash = _ipfs_public_key_hash;
        price = _price;
        description = _description;
    }
    
    function deposit() onlyBuyer external payable {
        require(currState == State.AWAITING_PAYMENT, "Already paid");
        currState = State.COMPLETE;
    }
    
    
}
