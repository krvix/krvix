// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChain {
    struct Product {
        uint256 id;
        string name;
        address manufacturer;
        string batchNumber;
        uint256 timestamp;
        string status;
        bool exists;
    }

    struct TrackingEvent {
        uint256 timestamp;
        string location;
        string eventType;
        string additionalData;
    }

    mapping(uint256 => Product) public products;
    mapping(uint256 => TrackingEvent[]) public productHistory;
    mapping(address => bool) public authorizedManufacturers;

    address public owner;

    event ProductCreated(uint256 indexed productId, string name, address manufacturer);
    event StatusUpdated(uint256 indexed productId, string status);
    event TrackingEventAdded(uint256 indexed productId, string location, string eventType);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedManufacturers[msg.sender], "Not authorized");
        _;
    }

    modifier productExists(uint256 productId) {
        require(products[productId].exists, "Product does not exist");
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedManufacturers[msg.sender] = true;
    }

    function authorizeManufacturer(address manufacturer) public onlyOwner {
        authorizedManufacturers[manufacturer] = true;
    }

    function revokeManufacturer(address manufacturer) public onlyOwner {
        authorizedManufacturers[manufacturer] = false;
    }

    function createProduct(
        uint256 productId,
        string memory name,
        string memory batchNumber
    ) public onlyAuthorized {
        require(!products[productId].exists, "Product already exists");

        products[productId] = Product({
            id: productId,
            name: name,
            manufacturer: msg.sender,
            batchNumber: batchNumber,
            timestamp: block.timestamp,
            status: "manufactured",
            exists: true
        });

        emit ProductCreated(productId, name, msg.sender);
    }

    function updateProductStatus(
        uint256 productId,
        string memory status
    ) public onlyAuthorized productExists(productId) {
        products[productId].status = status;
        emit StatusUpdated(productId, status);
    }

    function addTrackingEvent(
        uint256 productId,
        string memory location,
        uint256 timestamp,
        string memory eventType,
        string memory additionalData
    ) public onlyAuthorized productExists(productId) {
        TrackingEvent memory event = TrackingEvent({
            timestamp: timestamp,
            location: location,
            eventType: eventType,
            additionalData: additionalData
        });

        productHistory[productId].push(event);
        emit TrackingEventAdded(productId, location, eventType);
    }

    function getProduct(uint256 productId) public view productExists(productId) returns (
        uint256 id,
        string memory name,
        address manufacturer,
        string memory batchNumber,
        uint256 timestamp,
        string memory status
    ) {
        Product memory product = products[productId];
        return (
            product.id,
            product.name,
            product.manufacturer,
            product.batchNumber,
            product.timestamp,
            product.status
        );
    }

    function getProductHistory(uint256 productId) public view productExists(productId) returns (TrackingEvent[] memory) {
        return productHistory[productId];
    }

    function verifyProduct(uint256 productId) public view productExists(productId) returns (bool) {
        return products[productId].exists;
    }
}