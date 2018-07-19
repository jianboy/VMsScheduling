package me.yoqi.test;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

/**
 * 官方文档：http://commons.apache.org/proper/commons-csv/user-guide.html
 * 还有一个javacsv包更人性化。
 * @author liuyuqi
 *
 */
public class CSVOperation {

	public void write() {
		
	}
	public void read() throws IOException {
		Reader in = new FileReader("path/to/file.csv");
		Iterable<CSVRecord> records = CSVFormat.EXCEL.parse(in);
		for (CSVRecord record : records) {
		    String lastName = record.get("Last Name");
		    String firstName = record.get("First Name");
		}
	}
}
