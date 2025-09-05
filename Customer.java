import java.util.ArrayList;
class Customer{
    // atrtibutes
    private String password;
    private ArrayList<Order> orders = new ArrayList<>();

    // default constructor
    Customer(){
        this.password = "";
        orders = new ArrayList<>();
    }
    // overloaded constructor
    Customer(String password, ArrayList<Order> orders){
        this.password = password;
        this.orders = orders;
    }
    // constructor for password
    Customer(String password){
        this();
        this.password = password;
    }

    // getter for password
    public String getPassword(){
        return this.password;
    }
    // getter for order
    public ArrayList<Order> getOrders(){
        return this.orders;
    }
    // setter for order
    public void setOrders(ArrayList<Order> orders){
        this.orders = orders;
    }
    // add method
    public void addOrders(Order order){
        orders.add(order);
    }
    // removal method
    public void removeOrders(Order order){
        orders.remove(order);
    }


    
}