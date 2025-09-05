class Node {

    // members
    private Node next; // pointer to next node
    private Seat payload; // seat stored in the node

    // Default constructor
    public Node() {
        this.next = null;
        this.payload = null;
    }

    // Overloaded constructor
    public Node(Node next, Seat payload) {
        this.next = next;
        this.payload = payload;
    }

    // Mutators
    public void setNext(Node next) {
        this.next = next;
    }

    public void setPayload(Seat payload) {
        this.payload = payload;
    }

    // Accessors
    public Node getNext() {
        return next;
    }

    public Seat getPayload() {
        return payload;
    }

    // Returns node's contents as a string
    public String toString() {
        if (payload != null) {
            return payload.toString();
        } else {
            return "emplty node"; // Display error msg if there's no "Seat" in a node
        }
    }

}