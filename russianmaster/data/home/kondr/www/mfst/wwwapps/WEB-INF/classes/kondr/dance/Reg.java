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
	RegData regData;
	final String formFile="/reg/form.html";
	
	public Reg(){
		template=new KPageTemlate();
		regData=new RegData();
	}
	

	@Override
	public void init(ServletConfig cnf) throws ServletException 
	{
		super.init(cnf);
		contentType="text/plain; charset=windows-1251";//cp1251 utf-8 windows-1251
		characterEncodingIn="cp1251";
		characterEncodingOut="cp1251";
		path=context.getRealPath("/");
		
		template.prepare(path+formFile,"utf-8");
		regData.refreshData();
		
	}

	@Override
	public void httpGet(HttpData http) throws SQLException, ServletException,
			IOException
	{
		http.response.setContentType("text/html; charset=windows-1251");
        http.setHeader(RsH_CacheControl, "private,no-cache,no-store");		
		String info[]=http.getUrlExtraParams();	
		if (info==null || info.length < 2){http.write("<htnl><body><h3>Отсутсвуют параметры в адресе страницы</h3></body></htnl>");	return;}
		
		//Регистрационная форма http://rm8/java/reg/form/118	
		if (info[0].equals("form") && info[1].matches("\\d+"))
		{
			//template.prepare(path+"/reg/form.html","utf-8");
			
			String ins[]=new String[1];
			ins[0]="var CMP1="+dba.getDbString("cup", "SELECT CONCAT(\"new CMP('\",CAST(datestart AS CHAR),\"',\",CAST(id AS CHAR),\",'\",CAST(upd AS CHAR),\"',\",jsdata,\")\") FROM xcalendar"
												+" WHERE id = "	+ info[1]);
			http.writeTemplate(template,ins);
			
		}
		//Перезагрузка данных http://rm8/java/reg/reset/123
		else if (info[0].equals("reset") && info[1].equals("123"))
		{
			template.prepare(path+formFile,"utf-8");
			http.write("<htnl><body><h3>Данные обновлены</h3></body></htnl>");
		}
		else http.write("<htnl><body><h3>Не правильный адрес страницы</h3></body></htnl>");
	}

	@Override
	public void httpPost(HttpData http) throws SQLException, ServletException,
			IOException
	{
        http.setHeader(RsH_CacheControl, "private,no-cache,no-store");		
		String info[]=http.getUrlExtraParams();	
		if (info==null || info.length < 2){http.write("alert('Отсутсвуют параметры в адресе запроса');");	return;}
		
		//Партнеры http://rm8/java/reg/men/1050 (1050 - код первой заглавной буквы)
		if (info[0].equals("men") && info[1].matches("\\d+"))
		{
			int key=Integer.parseInt(info[1]);
			http.write(regData.getMen(key));
		}
		//Партнерши http://rm8/java/reg/wom/1050 (1050 - код первой заглавной буквы)
		else if (info[0].equals("wom") && info[1].matches("\\d+"))
		{
			int key=Integer.parseInt(info[1]);
			http.write(regData.getMen(key));
		}
		//Регионы http://rm8/java/reg/area/1050 (1050 - код первой заглавной буквы)		
		else if (info[0].equals("area") && info[1].matches("\\d+"))
		{
			int key=Integer.parseInt(info[1]);
			http.write(regData.getMen(key));
		}
		//Тренеры http://rm8/java/reg/trn/x
		else if (info[0].equals("trn"))
		{
			http.write(regData.getTreiner());
		}
		//Клубы http://rm8/java/reg/trn/x
		else if (info[0].equals("club"))
		{
			http.write(regData.getClub());
		}
		//Страны http://rm8/java/reg/trn/x
		else if (info[0].equals("cntr"))
		{
			http.write(regData.getCountry());
		}		
	}
}
