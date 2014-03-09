package kondr.dance;

import java.io.*;
import java.sql.*;
import javax.servlet.*;

import kondr.KServlet.KServlet;
/**
 * KServlet demo
 * @author kondr
 */
public class JsServlet extends KServlet implements Servlet 
{
	private static final long serialVersionUID = 1L;
       
	private int count=0;
	
	@Override
	public void init(ServletConfig cnf) throws ServletException 
	{
		super.init(cnf);
		contentType="text/html; charset=utf-8";//cp1251 utf-8 windows-1251
		characterEncodingIn="utf-8";
		characterEncodingOut="utf-8";
	}
	
	@Override
	public void httpGet(KServlet.HttpData http) throws SQLException, ServletException, IOException
	{
		http.setCookie("MyCookie", "value"+count);
		
		
		http.write("JsServlet 10 привет!!! "+(count++)+"<br>\n<br>\n<br>\n");
		http.writeTestForm();
		http.writeTestFormMultipart();
		
		//http.writeFromFile(context.getRealPath("/txt458.txt"));
		
		http.writeStringFromDB("test", "SELECT mystr FROM testcp1251 WHERE id=2");
					
		http.writeJSArray("test", "SELECT * FROM testcp1251 ","MI");
		
		http.requestToConsole(false, true, false);
			
		/*
		QueryResult qr = dba.executeQuery("test","SELECT * FROM untitled");
        ResultSet rs=qr.getResultSet();
		while (rs.next()) http.write(rs.getString(1)+""+rs.getString(2)+"<br>\n");
		qr.close();
		//*/
	}


	@Override
	public void httpPost(KServlet.HttpData http) throws SQLException, ServletException, IOException
	{
		http.write("httpPost! "+(count++)+"<br>\n<br>\n<br>\n");
		http.writeTestForm();
		http.writeTestFormMultipart();
		
		http.requestToConsole(false, true, false);
	}
	
	@Override
	public String saveFileRequest(String fileName, String formName)
	{
		return "d:\\delMe.txt";
	}


}
