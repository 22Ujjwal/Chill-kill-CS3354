class Seat {
    // private memebers
    private int row;    // rows
    private char seat;  // seat positions
    private char ticket_type;   // type of ticket (A,C,S)

    // default constructor
    // initialize int variable to 0, characters to null
    Seat() {
        row = 0;
        seat = '\0';
        ticket_type = '\0';
    }

    // overloaded constructor
    Seat(int row, char seat, char ticket_type) {
        this.row = row;
        this.seat = seat;
        this.ticket_type = ticket_type;
    }

    // mutators: set each variable to the value being passed into them, respectively
    public void setRow(int row) {
        this.row = row;
    }

    public void setSeat(char seat) {
        this.seat = seat;
    }

    public void setTicketType(char ticket_type) {
        this.ticket_type = ticket_type;
    }

    // accessors: access each variable
    public int getRow() {
        return row;
    }

    public char getSeat() {
        return seat;
    }

    public char getTicket_Type() {
        return ticket_type;
    }

    // returns ticket type as a string
    public String toString() {
        return String.valueOf(ticket_type);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Seat)) return false;
        Seat s = (Seat) o;
        return row == s.row && seat == s.seat;   // ignore ticket‑type
    }
    
}
