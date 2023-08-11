package java2;

import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

public class file1 {
	 public static void main(String[] args) throws IOException {
		 	String url = "https://www.mse.mn/mn";
		 	Document doc = Jsoup.connect(url).get();
	
		 	Elements body = doc.select("table.table.dividend.trade_table").first();
		 	System.out.println(body);
		    
		 	
		 	System.out.print("hello");
	   }
}
