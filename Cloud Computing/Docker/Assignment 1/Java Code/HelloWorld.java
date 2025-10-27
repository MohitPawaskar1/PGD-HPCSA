import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class HelloWorld {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8001), 0);
        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                exchange.getResponseHeaders().set("Content-Type", "text/html");
                String htmlResponse = "<html><body><h1>Hello, World!</h1></body></html>";
                byte[] responseBytes = htmlResponse.getBytes();
                exchange.sendResponseHeaders(200, responseBytes.length);
                OutputStream responseBody = exchange.getResponseBody();
                responseBody.write(responseBytes);
                responseBody.close();
            }
        });
        server.start();
        System.out.println("Server is listening on port 8001...");
    }
}
