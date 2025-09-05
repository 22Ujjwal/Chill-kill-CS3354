import java.util.ArrayList;
class Order {
	int audiNum;
	ArrayList<Seat> seats;
	int A_count, C_count, S_count;

	Order() { // default constructor
		audiNum = 0;
		seats = new ArrayList<>(); // arraylist of seat
		A_count = 0;
		C_count = 0;
		S_count = 0; // counter to keep track of ticket count for each type
	}

	// overloaded dconstrctor
	Order(int audiNum, ArrayList<Seat> seats, int A_count, int C_count, int S_count) {
		this.audiNum = audiNum;
		this.seats = seats;
		this.A_count = A_count;
		this.C_count = C_count;
		this.S_count = S_count;
	}

	// getter for audiNum
	public int getAudiNum() {
		return this.audiNum;
	}
	public ArrayList<Seat> getSeatList() {
		return seats;
	}
	public int getA_Count()       {
		return A_count;
	}
	public int getC_Count()       {
		return C_count;
	}
	public int getS_Count()      {
		return S_count;
	}

	@Override
	public String toString() {

		StringBuilder sb = new StringBuilder();
		sb.append("Auditorium ").append(audiNum).append(", ");
		for (int i = 0; i < seats.size(); i++) {
			Seat s = seats.get(i);  // obtain current seat position from list of seats
			sb.append(s.getRow()).append(s.getSeat());
			if (i != seats.size() - 1) sb.append(","); // process last line separately
		}
		sb.append("\n")
		.append(A_count).append(" adult, ")
		.append(C_count).append(" child, ")
		.append(S_count).append(" senior");
		return sb.toString();
	}

	public void addSeats(ArrayList<Seat> newSeats, int a, int c, int s) {
		seats.addAll(newSeats); // append new seats to existing list
		A_count += a;
		C_count += c;
		S_count += s;
	}

	public boolean containsSeat(Seat s) {
		for (Seat seat : seats)
		if (seat.equals(s)) {
		    return true;
		}
		return false;
	}

	public void removeSeats(ArrayList<Seat> deleteSeat) {
		Seat seatToDelete = deleteSeat.get(0);
		for (int i = 0; i < seats.size(); i++) { // traverse array list of seats
			// find seat to delete
			Seat s = seats.get(i);
			if (s.equals(seatToDelete)) {
				char type = s.getTicket_Type();
				seats.remove(i);
				if (type == 'A')  {
					A_count--;
				}
				else if (type == 'C') {
					C_count--;
				}
				else if (type == 'S') {
					S_count--;
				}
				break; // exits loop once seat to delete is found
			}
		}
	}

	public double calculateTotal() {
		return (10 * A_count + 5 *  C_count + 7.5 * S_count);
	}

}