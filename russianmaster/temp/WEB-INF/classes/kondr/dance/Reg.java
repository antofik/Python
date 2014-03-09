package kondr.dance;

import java.io.IOException;
import java.sql.SQLException;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;

import kondr.KServlet.KPageTemlate;
import kondr.KServlet.KServlet;

public class Reg extends KServlet
{
	String path;
	String formHtml;
	String headerHtml;
	String footerHtml;
	String javaScript;
	KPageTemlate template;
	

	@Override
	public void init(ServletConfig cnf) throws ServletException 
	{
		super.init(cnf);
		contentType="text/plain; charset=cp1251";//cp1251 utf-8 windows-1251
		characterEncodingIn="cp1251";
		characterEncodingOut="cp1251";
		path=context.getRealPath("/");
		template=new KPageTemlate();
		
		template.prepare(path+"/reg/form.html","utf-8");
	}

	@Override
	public void httpGet(HttpData http) throws SQLException, ServletException,
			IOException
	{
		http.response.setContentType("text/html; charset=cp1251");
        http.setHeader(RsH_CacheControl, "private,no-cache,no-store");
		
		String info[]=http.getUrlExtraParams();	
		if (info==null || info.length < 2){http.write("<htnl><body><h3>Отсутсвуют параметры в адресе страницы</h3></body></htnl>");	return;}
		
		//Регистрационная форма (http://rm8/java/reg/form/118)
		if (info[0].equals("form") && info[1].matches("\\d+"))
		{
			template.prepare(path+"/reg/form.html","utf-8");
			
			int cmp_id=Integer.parseInt(info[1]);
			String ins[]=new String[1];
			
			ins[0]=dba.getDbString("cup", "SELECT CONCAT(\"new CMP('\",CAST(datestart AS CHAR),\"',\",CAST(id AS CHAR),\",'\",CAST(upd AS CHAR),\"',\",jsdata,\")\") FROM xcalendar"+" WHERE id = "+cmp_id);
			
			http.writeTemplate(template,ins);
			
		}
		else http.write("<htnl><body><h3>Не правильный адрес страницы</h3></body></htnl>");

	}

	@Override
	public void httpPost(HttpData http) throws SQLException, ServletException,
			IOException
	{
		// TODO Auto-generated method stub

	}

}
