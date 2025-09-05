import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

class Auditorium{
    // Members
	private ArrayList<Node> rows; // Array list that contains head nodes of each row
	private int audiNum;

	// Constructor
	public Auditorium(int audiNum, String fileName) {
		this.audiNum = audiNum;
		rows = new ArrayList<>();
		readFile(audiNum, fileName);     // Read file
	}

	// Method to read data from file
	public void readFile(int audiNum, String fileName) {
		int rowCount = 0;   // starting row count
		try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
			String line;

            // Read each line from file
			while ((line = reader.readLine()) != null) {

				Node head = null;
				Node curr = null;
                
                // Traverse until end of line
				for (int i = 0; i < line.length(); i++) {

                    // Determine the type of ticket at index i
					char ticket_type = line.charAt(i); 

					// Store character in seat object
					Seat seat = new Seat(rowCount + i, (char) ('A' + i), ticket_type);

					// Store seat in new node
					Node newNode = new Node(null, seat);

                    // If list is empty, make head node the new node
					if (head == null) {
						head = newNode; 
						curr = head;      // make curr point to head

					} else { // Else append new node to the list
						curr.setNext(newNode); // Make curr point to new Node
						curr = newNode; // Set current nod eas new node



					}
				}
				rows.add(head); // add new row (lniked list) to arraylist
				rowCount++; // increment row count for tracking
			}

		} catch (IOException e) { 
			e.printStackTrace();   // Print error msgs if cannot read data from file
		}

	}

    // Method to convert seating
	public String toString() {

        // Build a string
		StringBuilder sb = new StringBuilder();

        // Traverse rows
		for (int i = 0; i < rows.size(); i++) {
			Node node = rows.get(i); // Obtain head node for each row

            // Traverse linked list (columns)
			while (node != null) {
                // Call toString() method of Node class, which calls toString() method of Seat class
				sb.append(node.toString());

				node = node.getNext(); // Move to next node
			}
			sb.append("\n"); // add new line character at the end of each row
		}

		return sb.toString(); // Return a string representation of the seating chart
	}

	// Method to display the chart
	public void printList() {
		int count = 1;
		char seatletter = 'A';

		System.out.print("   ");

        // Display seat letter at the top and row position at the left
		for (int i =0; i < rows.size(); i++) {
			System.out.print(seatletter);
			seatletter++;
		}
		System.out.println();
		for (int i = 0; i < rows.size(); i++) {
			System.out.print(count + ". ");
			count++;

			// get head node of the row
			Node node = rows.get(i);

            // traverse the row
			while (node != null) {

				// print data at current node then move to next node
				if (node.getPayload().getTicket_Type() != '.' ) {
					// If A,C,S encountered, mask with '#' to display to user
                    System.out.print('#');

				} else {
                    // print '.'
					System.out.print(node.getPayload().getTicket_Type());
				}

				node = node.getNext(); // move to next node
			}
			System.out.println(); // print new line
		}
	}

	// Method to validate seats. Return true if seat is found and false otherwise
	public boolean validateSeat(int userRow, char userSeat, int totalSeats) {

		int rowPos = userRow - 1; // target row
		int col_startPos = userSeat - 'A'; // starting position of the block
		int col_endPos = col_startPos + (totalSeats - 1); ///ending position of the block

		// position counter
		int pos = 0;

		// get the head node of targeted row position
		Node curr = rows.get(rowPos);

		// traverse the linked list until colPos is reached
		while (curr != null && pos < col_startPos) {
			curr = curr.getNext(); // move to next node
			pos++; // increment position
		}

		// traverse the list from pos to endPos
		while (curr != null && pos <= col_endPos) {

            // check if current seat is reserved
			if (curr.getPayload().getTicket_Type() != '.') {
				return false; // return false if seats are reserved
			}
			curr = curr.getNext(); // move to next node
			pos++;
		}
		return true;  // return true if seats are empty
	}

    // Method to reserved seats
	public void reserveSeats(int adultTickets, int childrenTickets, int seniorTickets, int userRow,
	                         char userSeat) {
		int rowPos = userRow - 1;   // starting row position
		int col_startPos = userSeat - 'A'; // starting position of target seat
		int cursor = 0; // cursor to move through the row

		// get rowPos
		Node curr = rows.get(rowPos);

		// move current node to targeted position
		while (curr != null && cursor < col_startPos) {
			curr = curr.getNext(); // move to next node
			cursor++; // increment cursor position by 1
		}

        // reserve seats for adults
		while (curr != null && cursor < adultTickets + col_startPos) { // traverse within the range of # of adult seats
			curr.getPayload().setTicketType('A');
			curr = curr.getNext(); // move to next seat to continue reservation
			cursor++;
		}

        // reserve seats for children
		while (curr != null && cursor < childrenTickets + col_startPos + adultTickets) { // traverse within the range of # of children seats
			curr.getPayload().setTicketType('C');
			curr = curr.getNext(); // move to next seat to continue reservation
			cursor++;
		}

        // reserve seats for seniors
		while (curr != null && cursor < seniorTickets + col_startPos + adultTickets + childrenTickets) { // traverse within the range of # of senior seats
			curr.getPayload().setTicketType('S');
			curr = curr.getNext(); // move to next seat to continue reservation
			cursor++;
		}
	}

	// method to delete tickets from auditorium
    public void deleteTickets(Seat seat){
        int rowIdx = seat.getRow() - 1;         
        if (rowIdx < 0 || rowIdx >= rows.size()) return;  // safety check

        Node curr = rows.get(rowIdx);
        while (curr != null) {
            if (curr.getPayload().getSeat() == seat.getSeat()){
                curr.getPayload().setTicketType('.');
                break;
            }
        curr = curr.getNext();
    }
}
    // Method to find number of columns in the grid
	public int colCount() {
		Node curr = rows.get(0);
		int colCount = 0;

        // traverse the linked list until end of node while keeping track of column count
		while (curr != null) {
			colCount++;
			curr = curr.getNext();
		}
		return colCount; // return number of columns counted
	}

    // Method to find number of rows in the grid
	public int getRows() {
		return rows.size(); // return number of rows counted
	}

   

	public double[] audiData(){ // helper method to print report for admin
		int adultTickets = 0;
		int childrenTickets = 0;
		int seniorTickets = 0;

		int colCount = colCount();  // obtain number of columns
		int totalSeat = rows.size() * colCount; // Compute total seats in the grid
		int totalTickets = 0;

        // Traverse array list
		for (int i = 0; i < rows.size(); i++) {

            // obtain head node
			Node curr = rows.get(i);

            // traverse each row
			while (curr != null) {
				char ticketType = Character.toUpperCase(curr.getPayload().getTicket_Type()); // identify current seat's type

                // keep track of the amount of tickets  sold for each category
				if (ticketType == 'A') {
					adultTickets++;
					totalTickets++;
				} else if (ticketType == 'C') {
					childrenTickets++;
					totalTickets++;
				} else if (ticketType == 'S') {
					seniorTickets++;
					totalTickets++;
				}

				curr = curr.getNext(); // move to next seat
			}
		}

        // compute total sales
		double totalSales = (adultTickets * 10.0) + (childrenTickets * 5.0) + (seniorTickets * 7.5);
		
		// comput # of open seat
		int openSeats = totalSeat - totalTickets;

		// print formatted report
		// return "Open #" + openSeats + '\t' + "Reserved #" + totalTickets + '\t' + "Adult #" + adultTickets + '\t'
        //        + "Child #" +  childrenTickets + '\t' + "Senior #" + seniorTickets + '\t' + "$" + rounded_totalSales;
		return new double[] {openSeats, totalTickets, adultTickets, childrenTickets, seniorTickets, totalSales};
	}

    // Metohd  to write chart to a seperate file
	public void writetoFile() {

        String outFile = "A" + audiNum + "Final.txt";
		try (PrintWriter writer = new PrintWriter(new FileWriter(outFile))) {

            // Traverse array list
			for (int i = 0; i < rows.size(); i++) {
				Node curr = rows.get(i);

                // Traverse linked list
				while (curr != null) {

                    // Print the node's content
					writer.print(curr.getPayload().getTicket_Type());
					curr = curr.getNext();
				}
				writer.println(); // Move to next line
			}
		} catch (IOException e) {
			System.out.println("Error writing to file");
		}

	}

    // Method to find best seats available by retuning the column of row position of the block of seat
	public int[] bestAvailable(int totalSeats) {

		// Get the x and y coordinates of auditorium's center
		int row = getRows();
		int col = colCount();

		// Ensure totalSeats is valid
		if (totalSeats > col) {
			System.out.println("Invalid request: totalSeats is greater than column count.");
			return null;
		}

		int x_audi; // x coordinate of auditorium (center col)

        // Compute the center accordingly to even or odd row length
		if (col % 2 == 1) {  // Odd number of columns
			x_audi = (col / 2) - 1;
		} else {  // Even number of columns
			x_audi = (col - 1)/ 2;
		} // Center seat (column)

		int y_audi = row / 2; // y coordinate of auditorium (center row)

		// Print auditorium center coordinates
		System.out.printf("Auditorium Center: (%d, %d)\n", x_audi, y_audi);

		double min = Double.MAX_VALUE; // Initialize minimum distance to max value
		int bestRow = -1; // Starting row pos of recommened seat
		int bestCol = -1; // Starting col pos of recommened seat

		// Traverse each row
		for (int i = 0; i < rows.size(); i++) {
			Node curr = rows.get(i); // Head of the current row
			int startPos = 0; // Starting position in the row

			// Traverse each possible starting position in the row
			while (curr != null && startPos <= (col - totalSeats)) {
				boolean isEmpty = true;
				Node temp = curr; // Temporary node to check the block of seats

				// Traverse within the range of user's requested seats
				for (int j = 0; j < totalSeats; j++) {

                    // If one seat is reserved
					if (temp == null || temp.getPayload().getTicket_Type() != '.') {
						isEmpty = false; // Block is invalid
						break;
					}
					temp = temp.getNext(); // Move to next seat
				}

                // If block is valid
				if (isEmpty) { 
					// Compute the center of the block
					int x_block = startPos + ((totalSeats-1) / 2);
					int y_block = i;

					// Compute distance
					double distance = Math.sqrt(Math.pow((x_audi - x_block), 2) + Math.pow((y_audi - y_block), 2));

                    // Find block of seats with minimum distance and update its row and column positions accordingly
					if (distance < min) {

						min = distance; // Set new minimum distance
						bestRow = i;    // Row position of the block
						bestCol = startPos; // Column position of the block

					} 
                    // If a tie for distance is found
                    else if (distance == min) {

                        // Calculate best row's distance from center row
						int currentRowDist = Math.abs(y_audi - bestRow);

                         // Calculate current row's distance from center row
						int newRowDist = Math.abs(y_audi - i);

                        // If current row's distance is less than best row's distance, choose current row
						if (newRowDist < currentRowDist) {

                            // Record current row's row and col pos
							bestRow = i;
							bestCol = startPos;

						} 
                        //  If current row's distance is equal to best row's distance, choose one with smaller number
                        else if (newRowDist == currentRowDist) {

                            // Record current row's col and row pos if its number is less than best row
							if (i < bestRow) {
								bestRow = i;
								bestCol = startPos;
							}
						}
					}
				}

				// Move to the next seat
				startPos++; // Move to next starting position in the linked list
				curr = curr.getNext(); // Move to next node
			}
		}

		if (bestRow == -1) { // If no available seats is found, print msg and return null
			System.out.println("No available seats found.");
			return null;

		} else { // Return array that contains best seat's row and col positions
			System.out.printf("Final Best Seat: Row %d, Column %c\n", (bestRow + 1), (char)('A' + bestCol));
			return new int[] {bestRow, bestCol};
		}
	}

}