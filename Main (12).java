// Name: Thu Huong Huynh
// NetID: txh230016
import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.NoSuchElementException;

public class Main {
	public static void main(String[] args) {
	    // copy any existing A#Final.txt files to A#.txt first
        copyFinalFilesToOriginal();
		HashMap<String, Customer> database = new HashMap<>(); // map to store customer's info with order info

		// create Auditorium object
		Auditorium audi1 = new Auditorium(1, "A1.txt");
		Auditorium audi2 = new Auditorium(2, "A2.txt");
		Auditorium audi3 = new Auditorium(3, "A3.txt");

		// open userdatabase file
		File userdb = new File("userdb.dat");
		// read userdb.dat
		processUserFile(userdb, database);
		Scanner sc = new Scanner(System.in);

		// ***************** PRINT LOGIN MENU ***************************************

		while (true) {
			// Prompt for username
			System.out.print("Enter username: ");
            if (!sc.hasNextLine()) {   // eof check
                            System.out.print("end of file."); 
                            sc.close(); 
                            return;                
                        }
			String usernameInput = sc.nextLine();
			Customer customer = database.get(usernameInput);

			if (customer == null) {
				System.out.println("Invalid username.");
				continue;   // back to username prompt
			}

			// 3 tries to enter the correct password
		    int counter = 0; // counter to count number of invalid attempts
			boolean loggedIn = false;
			while (counter < 3) {
				System.out.print("Enter password: ");
                if (!sc.hasNextLine()) {   // eof check
                            System.out.print("end of file.");  
                            return;                
                        }
				String passwordInput = sc.nextLine();
				if (customer.getPassword().equals(passwordInput)) {
					System.out.println("Logged in successfully.");
					loggedIn = true;
					break;
				} else {
					counter++; // count attmpets
					System.out.println("Invalid password entered.");
				}
			}

			if (!loggedIn) {
				System.out.println("Too many failed attempts. Returning to login menu.\n");
				continue;   // go back to username prompt
			}

			// dispatch to the correct UI
			if (usernameInput.startsWith("admin")) {
				adminUI(sc, audi1, audi2, audi3);
			} else {
				customerUI(sc, audi1, audi2, audi3, customer);
			}
			// when either UI returns (logout), we loop back and prompt for username again
		}
        
	}
	
	public static void copyFinalFilesToOriginal() {
    for (int i = 1; i <= 3; i++) {
        String finalFileName = "A" + i + "Final.txt";
        String originalFileName = "A" + i + ".txt";
        
        File finalFile = new File(finalFileName);
        if (finalFile.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(finalFileName));
                 PrintWriter writer = new PrintWriter(new FileWriter(originalFileName))) {
                
                String line;
                while ((line = reader.readLine()) != null) {
                    writer.println(line);
                }
                System.out.println("Copied " + finalFileName + " to " + originalFileName);
            } catch (IOException e) {
                System.out.println("Error copying " + finalFileName + " to " + originalFileName + ": " + e.getMessage());
            }
        }
    }
}

	// ============================ Process userdb.dat
	// =================================

	public static void processUserFile(File userdb, HashMap<String, Customer> database) {
		String line; // String to store user info
		try (BufferedReader br = new BufferedReader(new FileReader(userdb))) {
			while ((line = br.readLine()) != null) {
				// split into 2 fields
				String[] parts = line.split(" "); // split by space
				String username = parts[0]; // username
				String password = parts[1]; // password

				// username = key, pass word = value (in Customer)
				Customer customer = new Customer(password); // pass password into Customer class
				database.put(username, customer); // add updated customer info to database

			}
		} catch (Exception e) {
			System.out.println("Error reading file.");
		}
	}

	// ***************************** CUSTOMER USER INTERFACE
	// ********************************************//

	public static void customerUI(Scanner sc, Auditorium audi1, Auditorium audi2, Auditorium audi3, Customer customer) {
		int choice;// menu choice
		do {
			// display main menu
			System.out.println("1. Reserve Seats\r\n" +
			                   "2. View Orders\r\n" +
			                   "3. Update Order\r\n" +
			                   "4. Display Receipt\r\n" +
			                   "5. Log Out");

			// Get menu choice with validation
			do {
				System.out.print("Enter menu choice: ");
                if (!sc.hasNextLine()) {   // eof check
                            return;                  
                        }
				String choiceInput = sc.nextLine();
				try {
					choice = Integer.parseInt(choiceInput);
					if (choice < 1 || choice > 5) {
						System.out.println("Please enter a number between 1 and 5.");
						choice = -1;
					}
				} catch (NumberFormatException e) {
					System.out.println("Please enter a number between 1 and 5.");
					choice = -1;
				}
			} while (choice == -1);

			switch (choice) {
			case 1: { // action: reserve seats
				String prompt = "1. Auditorium 1\r\n" + //
				                   "2. Auditorium 2\r\n" + //
				                   "3. Auditorium 3\n";
	
				System.out.println("Enter an auditorium: ");
				int audiChoice;
				do {
					System.out.print(prompt);
                    if (!sc.hasNextLine()) {   // eof check
                            return ;                  
                        }
					String audiInput = sc.nextLine();
					try {
						audiChoice = Integer.parseInt(audiInput);
						if (audiChoice < 1 || audiChoice > 3) {
							System.out.println("Invalid input. Enter a number between 1 and 3.");
							audiChoice = -1;
						}
					} catch (NumberFormatException e) {
						System.out.println("Invalid input. Enter a number between 1 and 3.");
						audiChoice = -1;
					}
				} while (audiChoice == -1);
				
				// array to store ticket counts for each type (A/C/S)
				int[] storeCount = new int[3];

				Auditorium audi = null;
				// select auditorium based on choice
				switch (audiChoice) {
				case 1:
					audi = audi1;
					break;
				case 2:
					audi = audi2;
					break;
				case 3:
					audi = audi3;
					break;
				}

				// Print and process the selected auditorium
				audi.printList();
				ArrayList<Seat> seats = seatHelper(sc, audi, storeCount, "");
				if (seats != null && !seats.isEmpty()) {
					Order order = new Order(audiChoice, seats,
					                        storeCount[0], storeCount[1], storeCount[2]);
					customer.addOrders(order); // add to this customer
				}
			}
			break;
			case 2: // view order
			{	// retrieve customer info from hashmap
			    ArrayList<Order> orderList = customer.getOrders();
				if (orderList.isEmpty()) {
					System.out.println("No orders.");
				} else {
					for (int i = 0; i < orderList.size(); i++) {
						System.out.println(orderList.get(i).toString()); // print each order
					}
				}
			}
			break;
			case 3: // update order
			{
				// create a list of orders from customer
				ArrayList<Order> orderList = customer.getOrders();
				int orderCount = orderList.size();
				
                 if (orderList.isEmpty()) {
                    System.out.println("No orders.");
                 break;
                }
				for (int i = 0; i < orderList.size(); i++) {
					System.out.println((i + 1) + ". " + orderList.get(i).toString()); // print each order
				}
				
				// Get order number to modify
					int orderNum;
					do {
						System.out.print("Select order to modify: ");

                        if (!sc.hasNextLine()) {   // eof check
                            return;                  
                        }
						String orderNumInput = sc.nextLine();
						try {
							orderNum = Integer.parseInt(orderNumInput);  // valid input
							if (orderNum < 1 || orderNum > orderCount) {
								System.out.println("Invalid order number. Please enter 1-" + orderCount);
								orderNum = -1;
							} 
						} catch (NumberFormatException e) {
							System.out.println("Invalid order number. Please enter 1-" + orderCount);
							orderNum = -1;
						}
					} while (orderNum == -1);
				

				// Get update choice with validation
				int orderChoice;
				do {
					System.out.print("\n1. Add tickets to order\n2. Delete tickets from order\n3. Cancel Order\n");
					if (!sc.hasNextLine()) {   // eof check
                            return ;                  
                        }
                    String orderChoiceInput = sc.nextLine();
					try {
						orderChoice = Integer.parseInt(orderChoiceInput);
						if (orderChoice < 1 || orderChoice > 3) {
							System.out.println("Invalid input entered. Enter a number between 1 and 3.");
							orderChoice = -1;
						}
					} catch (NumberFormatException e) {
						System.out.println("Invalid input entered. Enter a number between 1 and 3.");
						orderChoice = -1;
					}
				} while (orderChoice == -1);

				// =============================== Add tickets to order
				// ===================================
				if (orderChoice == 1) { // action: add tickets to order
	

					// from user's order number, identify which index the order is located on the
					// orderList
					Order order = orderList.get(orderNum - 1);

					// obtain auditorium number from order
					int audiNum = order.getAudiNum();

					// reserve seat based on auditorium number
					Auditorium target = (order.getAudiNum() == 1) ? audi1
					                    : (order.getAudiNum() == 2) ? audi2 : audi3;
					int[] storeCount = new int[3]; // array to store ticket counts for each type (A/C/S)

					String command = "add"; // this tell seatHelper user is adding tickets to order, no
					// bestAvailable offer
					ArrayList<Seat> newSeats = seatHelper(sc, target, storeCount, command); // list of new seats

					// add new seats to order
					if (newSeats != null && !(newSeats.isEmpty())) {
						order.addSeats(newSeats, storeCount[0], storeCount[1], storeCount[2]);
					}

					// ========================= Deleting tickets
					// =====================================
				} else if (orderChoice == 2) { // action: delete tickets from order

					// from user's order number, identify which index the order is located on the
					// orderList
					Order order = orderList.get(orderNum - 1);

					// obtain auditorium number from order
					int audiNum = order.getAudiNum();
					Auditorium target = (order.getAudiNum() == 1) ? audi1
					                    : (order.getAudiNum() == 2) ? audi2 : audi3;

					// Get row to delete
					int userRow;
					do {
						System.out.print("Enter row to delete: ");
                        if (!sc.hasNextLine()) {   // eof check
                            return;                  
                        }
						String rowInput = sc.nextLine();  // Changed from sc.next() to sc.nextLine()
						try {
							userRow = Integer.parseInt(rowInput);
							if (userRow < 1 || userRow > target.getRows()) {
								System.out.println("seats not available");
								userRow = -1;
							}
						} catch (NumberFormatException e) {
							System.out.println("seats not available");
							userRow = -1;
						}
					} while (userRow == -1);

					// Get seat to delete
					char userSeat;
					do {
						System.out.print("Enter seat to delete: ");
                        if (!sc.hasNextLine()) {   // eof check
                            return;                  
                        }
						String seatInput = sc.nextLine();
						if (seatInput.length() == 1 && seatInput.charAt(0) >= 'A' && seatInput.charAt(0) <= ('A' + target.colCount() - 1)) {
							userSeat = seatInput.charAt(0);
							break;
						} else {
							System.out.println("Invalid seat letter.");
							userSeat = '\0';
						}
					} while (userSeat == '\0');
					
					// verify seat belongs to order
                    Seat requested = new Seat(userRow, userSeat, 'A');
                        if (!order.containsSeat(requested)) {       
                        System.out.println("Seat not found in this order.");
                        break;                                 // back to submenu
                        }

					// list to store seat(s) to delete
					ArrayList<Seat> seatToDelete = new ArrayList<>();
					seatToDelete.add(requested); // add seat to delete to array list

					// delete requested seat
					target.deleteTickets(requested);

					// update order once ticket(s) are deleted
					order.removeSeats(seatToDelete);

                     if (order.getA_Count() == 0 && 
                        order.getC_Count() == 0 && 
                        order.getS_Count() == 0) {
        
                    // order is empty - remove it from customer's orders
                        orderList.remove(orderNum - 1);
                    System.out.println("Order cancelled due to removal of all tickets.");
    }

					// ================================== Canceling order
					// ========================================
				} else if (orderChoice == 3) { // action: cancel order
					// Get order number to modify


					// from user's order number, identify which index the order is located on the
					// orderList
					Order order = orderList.get(orderNum - 1);

					// obtain auditorium number from order
					int audiNum = order.getAudiNum();
					Auditorium target = (order.getAudiNum() == 1) ? audi1
					                    : (order.getAudiNum() == 2) ? audi2 : audi3;

					// to cancel order, first unreserve all seats in ArrayList<Seat>
					// obtain list of seats from order
					ArrayList<Seat> seatList = order.getSeatList();

					// after obtain seatlist, traverse list
					for (Seat seat : seatList) {
						target.deleteTickets(seat); // unreserves every seats in the order
					}
					// remove order from customer's list of orders once unresevation is done
					orderList.remove(orderNum - 1);
				}
			}
			break;

			// =================================== Print receipt
			// ===========================================
			case 4: // print receipt
				printReceipt(customer);
				break;
			case 5: // exit
				return;
				// =================================== Logging out
				// =============================================
			}
		} while (choice != 5);
	}

	// helper method to help with seat processing. return an arraylist of Seat objects
	public static ArrayList<Seat> seatHelper(Scanner sc, Auditorium audi, int[] storeCount, String cmd) {
		// list of auditorium related variable
		int row; // row number
		char seat; // seat letter
		int A_ticket = 0, C_ticket = 0, S_ticket = 0; // adult, children, senior ticket

		int rows = audi.getRows();
		int cols = audi.colCount();

		// Get row number with validation
		do {
			System.out.print("Enter row number: ");
            if (!sc.hasNextLine()) {   // eof check
                            return null;                  
                        }
			String rowInput = sc.nextLine();
			try {
				row = Integer.parseInt(rowInput);
				if (row < 1 || row > rows) {
					System.out.println("seats not available");
					row = -1;
				}
			} catch (NumberFormatException e) {
				System.out.println("seats not available");
				row = -1;
			}
		} while (row == -1);

		// Get starting seat with validation
		while (true){
			System.out.print("Enter starting seat: ");
            if (!sc.hasNextLine()) {   // eof check
                            return null;                  
                        }
			String seatInput = sc.nextLine();
			if (seatInput.length() == 1 && seatInput.charAt(0) >= 'A' && seatInput.charAt(0) <= ('A' + cols - 1)) {
				seat = seatInput.charAt(0);
				break;
			} else {
				System.out.println("Invalid seat letter.");
			}
		} 

		// Get adult tickets
		do {
			System.out.print("Enter number of adult tickets: ");
            if (!sc.hasNextLine()) {   // eof check
                            return null;                  
                        }
			String adultInput = sc.nextLine();  // Changed from sc.next() to sc.nextLine()
			try {
				A_ticket = Integer.parseInt(adultInput);
				if (A_ticket < 0 || A_ticket > cols) {
					System.out.println("seats not available");
					A_ticket = -1;
				}
			} catch (NumberFormatException e) {
				System.out.println("seats not available");
				A_ticket = -1;
			}
		} while (A_ticket == -1);

		// Get children tickets
		do {
			System.out.print("Enter number of children tickets: ");
            if (!sc.hasNextLine()) {   // eof check
                            return null;                  
                        }
			String childInput = sc.nextLine();  // Changed from sc.next() to sc.nextLine()
			try {
				C_ticket = Integer.parseInt(childInput);
				if (C_ticket < 0 || C_ticket > cols) {
					System.out.println("seats not available");
					C_ticket = -1;
				}
			} catch (NumberFormatException e) {
				System.out.println("seats not available");
				C_ticket = -1;
			}
		} while (C_ticket == -1);

		// Get senior tickets
		do {
			System.out.print("Enter number of senior tickets: ");
            if (!sc.hasNextLine()) {   // eof check
                            return null;                  
                        }
			String seniorInput = sc.nextLine();  // Changed from sc.next() to sc.nextLine()
			try {
				S_ticket = Integer.parseInt(seniorInput);
				if (S_ticket < 0 || S_ticket > cols) {
					System.out.println("seats not available");
					S_ticket = -1;
				}
			} catch (NumberFormatException e) {
				System.out.println("seats not available");
				S_ticket = -1;
			}
		} while (S_ticket == -1);

		// compute total tickets
		int totalTickets = A_ticket + C_ticket + S_ticket;

		// pass to seat validation to confirm seat is valid and available
		boolean isAvailable = audi.validateSeat(row, seat, totalTickets);

		if (isAvailable) { // if seat available
			audi.reserveSeats(A_ticket, C_ticket, S_ticket, row, seat); // reserve seat
			System.out.println("reserved seats successfully.");

		} else if (!isAvailable && !cmd.equals("add")) { // only recommend unless user is adding tickets to their order

			// recommend best available seat.
			int[] bestSeat = audi.bestAvailable(totalTickets);

			if (bestSeat != null) { // if best seat is available
                // display best seats
                System.out.println("Best available seats start at: " + (bestSeat[0] + 1) + (char) ('A' + bestSeat[1]) + "-" + (bestSeat[0] + 1) + (char)('A' + bestSeat[1] + totalTickets - 1));

				String input;
				char action;
				do {
					System.out.print("Reserve seat? Y/N: ");
                    if (!sc.hasNextLine()) {   // eof check
                            return null;                  
                        }
					input = sc.nextLine().trim();
					if (input.length() > 0) {
						action = input.charAt(0);
						if (action == 'Y') { // if yes, reserve seat
							row = bestSeat[0] + 1;          // <-- convert back to 1‑based
							seat = (char) (bestSeat[1] + 'A');
							audi.reserveSeats(A_ticket, C_ticket, S_ticket, row, seat);
							System.out.println("reserved seats successfully.");
							break;
						} else if (action == 'N') {
						    return null;
						//	break; // break loop and return to main menu
						} else {
							System.out.print("Please enter Y/N.");
							action = '\0';
						}
					} else {
						action = '\0';
					}
				} while (action == '\0');
			} else if (!isAvailable) { // no seats available
				System.out.println("No available seats. ");
			}
		}

		// store counts for each ticket type
		storeCount[0] = A_ticket;
		storeCount[1] = C_ticket;
		storeCount[2] = S_ticket;

		char letter = seat; // starting seat letter

		ArrayList<Seat> block = new ArrayList<>(); // create an array list of seats
		for (int i = 0; i < A_ticket; i++, letter++) {
			block.add(new Seat(row, letter, 'A')); // add new seat obj, increment seat letter upto total number of
			// ticket
		}
		for (int i = 0; i < C_ticket; i++, letter++) {
			block.add(new Seat(row, letter, 'C'));
		}
		for (int i = 0; i < S_ticket; i++, letter++) {
			block.add(new Seat(row, letter, 'S'));
		}
		return block;
	}

	// helper method to print receipt
	public static void printReceipt(Customer customer) {
		// access customer's list of orders
		ArrayList<Order> orders = customer.getOrders();

		// total for all orders
		double totalOrders = 0;
		// for each order, print info
		for (Order order : orders) {
			System.out.println(order.toString());
			System.out.printf("Order Total: $%.2f\n\n",  order.calculateTotal());
			totalOrders += order.calculateTotal();
		}

		// display customer's total
		System.out.printf("Customer Total: $%.2f\n", totalOrders);
	}

	// ************************************** ADMIN USER INTERFACE
	// *******************************************//

	public static void adminUI(Scanner sc, Auditorium audi1, Auditorium audi2, Auditorium audi3) {
		int adminChoice;
		do {
			// Display admin menu:
			String prompt = "1. Print Report\r\n" + //
			                "2. Logout\r\n" + //
			                   "3. Exit";
			
			// Get admin choice with validation
			do {
				System.out.print(prompt + "\n");
                if (!sc.hasNextLine()) {   // eof check
                            return;                  
                        }
				String adminInput = sc.nextLine();  // Changed from sc.next() to sc.nextLine()
				try {
					adminChoice = Integer.parseInt(adminInput);
					if (adminChoice < 1 || adminChoice > 3) {
						System.out.println("Please enter a number between 1 and 3.");
						adminChoice = -1;
					}
				} catch (NumberFormatException e) {
					System.out.println("Please enter a number between 1 and 3.");
					adminChoice = -1;
				}
			} while (adminChoice == -1);

			switch (adminChoice) {
			case 1: // print report
				printReport(audi1, audi2, audi3);
				break;
			case 2: // logout
				System.out.println("logging out...");
				return; // return to logout menu
			case 3: // exit
			// write updated auditorium to new file names "A#Final.txt"
			audi1.writetoFile();
		    audi2.writetoFile();
		    audi3.writetoFile();
			System.exit(0);
			}
		} while (adminChoice != 3);
		
	}

	// helper method to print report
	public static void printReport(Auditorium audi1, Auditorium audi2, Auditorium audi3) {

		// create an array of Auditorium
		Auditorium[] audi = { audi1, audi2, audi3 };

		// total amount for each statistic across all auditorium
		int t_open = 0; // total open seats
		int t_reserved = 0; // total reserved seats
		int t_a = 0, t_c = 0, t_s = 0; // total tickets for each type
		double t_sales = 0; // total sales for all auditoriums

		for (int i = 0; i < audi.length; i++) {
			// process information for each field
			double[] data = audi[i].audiData();

			int openSeats = (int) data[0];
			t_open += openSeats;
			int reservedSeats = (int) data[1]; // toal amount of reserved seats
			t_reserved += reservedSeats;
			int adults = (int) data[2];
			t_a += adults;
			int children = (int) data[3];
			t_c += children;
			int seniors = (int) data[4];
			t_s += seniors;
			double totalSales = data[5];
			t_sales += totalSales;

			// print data summary for each auditorium
            System.out.printf("Auditorium %d\t%d\t%d\t%d\t%d\t%d\t$%.2f\n", (i + 1), openSeats, reservedSeats, adults, children, seniors, totalSales);
		}

		// data from all auditorium
        System.out.printf("Total\t%d\t%d\t%d\t%d\t%d\t$%.2f\n", t_open, t_reserved, t_a, t_c, t_s, t_sales);
	}
}