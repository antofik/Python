package kondr.dance;

import java.io.IOException;
import java.sql.SQLException;
import java.util.Date;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;

import kondr.KServlet.KServlet;

public class Forum extends KServlet
{
	@Override
	public void init(ServletConfig cnf) throws ServletException 
	{
		super.init(cnf);
		contentType="text/plain; charset=windows-1251";//cp1251 utf-8 windows-1251
		characterEncodingIn="windows-1251";
		characterEncodingOut="windows-1251";
	}
	
	@Override
	public void httpGet(HttpData http) throws SQLException, ServletException, IOException
	{
		http.response.setCharacterEncoding("utf-8");
		http.response.setContentType("text/html; charset=utf-8");
		
		http.writeFromFile(context.getRealPath("/")+"/forum/forum.html");
	}

	@Override
	public void httpPost(HttpData http) throws SQLException, ServletException, IOException
	{
		//Параметры, передаваемые в строке http запроса
		String info[]=http.getUrlExtraParams();
		
		if (info==null || info.length < 1)
		{
			http.write("alert('info type not define');");
			return;
		}
		
		//Запрос форума (http://rm8/java/forum/select/)
		if (info[0].equals("select"))
		{
			String time=http.getParametr("time");
			String part=http.getParametr("part");
			String timeFilter;
			String partFilter="";
			long curTime=new Date().getTime()/1000;
			
			if (!part.isEmpty() && part.matches("[\\d,]+")) partFilter=" AND temepart IN ("+part+")";
			
			if (!time.isEmpty() && time.matches("\\d+"))
			{
				if (time.equals("0"))
				{
					String previs=http.getParametr("previs");
					if (previs.isEmpty() || !time.matches("\\d+")) return;
					timeFilter=" WHERE temetime>"+previs;
				}
				else {				
					timeFilter=" WHERE temetime>"+(curTime-Integer.parseInt(time)*86400);
				}
			}
			else timeFilter=" WHERE temetime>"+(curTime-720*86400);
					
			String sql="SELECT idfm,idvip,part,teme,parid,status,cmplt,text,fmtime,nike,pubtime,voit1,voit0 FROM forum_time INNER JOIN forum_mes ON idteme = teme "+
						timeFilter+partFilter+
						" ORDER BY idfm";
			http.write("FMs=");
			http.writeJSArray("forum", sql, "FM");
		}
		
		else http.write("alert('no know params');");
	}
}
