package kondr.dance;

import java.io.IOException;
import java.sql.SQLException;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;

import kondr.KServlet.KServlet;

public class Cup extends KServlet
{
	String groupList="cCG={'63':'N9 и мл.','62':'N10-11','61':'N12-15','60':'N16 и ст.','54':'E9 и мл.','53':'E10-11','52':'E12-13','51':'E14-15','50':'E16 и ст.','43':'D11 и мл.','42':'D12-13','41':'D14-15','40':'D16 и ст.','32':'C13 и мл.','31':'C14-15','30':'C16 и ст.','20':'B16 и ст.','25':'A+B15 и мл.','10':'A16 и ст.','101':'Взрослые (21 и старше)','102':'Молодежь-2 (19-20)','103':'Молодежь-1 (16-18)','104':'Юниоры-2 (14-15)','106':'Юниоры-1 (12-13)','105':'Ювеналы-2 (10-11)','107':'Ювеналы-1 (9 и младше)'};";

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
		/*
		httpPost(http);
		/*/
		
		http.response.setCharacterEncoding("utf-8");
		http.response.setContentType("text/html; charset=utf-8");
		
		String info[]=http.getUrlExtraParams();
		
		if (info==null || info.length < 1)
		{
			http.write("<htnl><body><h3>Отсутсвуют параметры в адресе страницы</h3></body></htnl>");
			return;
		}
		
		//Страница рейтинга
		if (info[0].equals("rate")) http.writeFromFile(context.getRealPath("/")+"/cup/cup.html");
		
		//Страница календаря соревнований
		else if (info[0].equals("comp")) http.writeFromFile(context.getRealPath("/")+"/cup/comp.html");

		else http.write("<htnl><body><h3>Не правильно указаны параметры в адресе страницы</h3></body></htnl>");
		
		//*/
	}

	@Override
	public void httpPost(HttpData http) throws SQLException, ServletException, IOException
	{
		//Параметры, передаваемые в строке http запроса
		String info[]=http.getUrlExtraParams();
		
		if (info==null || info.length < 3)
		{
			http.write("alert('info type not define');");
			return;
		}
		
		//Запрос протокола (http://rm8/java/cup/prl/120/1)
		if (info[0].equals("prl"))
		{
			try
			{
				int id=Integer.parseInt(info[1]);
				http.writeStringFromDB("cup", "SELECT jsdata FROM xprotocol WHERE id="+id);
				http.write("\ncPrtReady('"+id+"',"+info[2]+");");
			}
			catch(NumberFormatException e){http.write("alert('protocol id not define');");}
			return;
		}
		
		//Запрос рейтинга (http://rm8/java/cup/rate/2012/51)
		else if (info[0].equals("rate"))
		{
			if (info[1].matches("\\d\\d\\d\\d") && info[2].matches("\\d+"))
			{
				http.write(groupList);
				http.writeStringFromDB("cup", "SELECT CONCAT(json,DATE_FORMAT(upd,\"\\ncUpd["+info[2]+"]='%Y-%m-%d %H:%i';\")) FROM xrating"+info[1]+" WHERE grp="+info[2]);
				http.write("\ncReady(true);");				
			}
			else
			{
				http.write("alert('rate id not define');");
			}
			return;
		}
		
		//Календарь - список соревнований (http://rm8/java/cup/comp/2011-08/2012-07)
		else if (info[0].equals("comp"))
		{
			if (info[1].matches("\\d\\d\\d\\d-\\d\\d") && info[2].matches("\\d\\d\\d\\d-\\d\\d"))
			{
				http.write(groupList);
				http.write("CMP.cmps=[\n");
				http.writeTextFromDB("cup", "SELECT CONCAT(\"new CMP('\",CAST(datestart AS CHAR),\"',\",CAST(id AS CHAR),\",'\",CAST(upd AS CHAR),\"',\",jsdata,\")\") FROM xcalendar"+
						" WHERE datestart >= \""+info[1]+"-1\" AND datestart < \""+info[2]+"-1\"",",\n\n");
				http.write("\n];\n");
			}
			else http.write("alert('date is not correct');");
			return;
		}
		else http.write("alert('no know params');");
	}
	
}
