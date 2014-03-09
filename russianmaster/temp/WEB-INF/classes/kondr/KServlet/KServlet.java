package kondr.KServlet;

import java.io.*;
import java.sql.*;
import java.util.*;
import java.util.Date;

import javax.servlet.*;
import javax.servlet.http.*;

import com.oreilly.servlet.*;
import com.oreilly.servlet.multipart.FilePart;
import com.oreilly.servlet.multipart.MultipartParser;
import com.oreilly.servlet.multipart.ParamPart;
import com.oreilly.servlet.multipart.Part;


/**
 * Базовый классс для создания севлетов
 * Упрощает типовые задачи при построении сервлетов.
 * @author kondr
 *
 */
public abstract class KServlet extends HttpServlet
{
	public static final String RsH_CacheControl = "Cache-Control";
	public static final String RsH_Expires = "Expires";
	
	protected String contentType;
	protected String characterEncodingIn;
	protected String characterEncodingOut;
	protected int maxMultipartSizeMb;
	protected int maxMultipartParams;
	protected DbAccess dba;
	protected ServletConfig config;
	protected ServletContext context;
	
	public KServlet()
	{
		super();
		dba=KContext.dba;
		contentType="text/html; charset=utf-8";
		characterEncodingOut="utf-8";
		characterEncodingIn="utf-8";
		maxMultipartSizeMb=10;
		maxMultipartParams=30;		
	}
	

	public abstract void httpGet(HttpData http) throws SQLException, ServletException, IOException;
	public abstract void httpPost(HttpData http) throws SQLException, ServletException, IOException;
	
	/**
	 * Для сохранения файлов данную функцию нужно переопределить в производном классе
	 * Функция должны проверять имя файла и имя элемента формы и возвращать полный путь и имя для сохранения файла 
	 * @param fileName Имя файла
	 * @param formName Имя элемента формы
	 * @return Путь для сохранения загружаемого файла
	 */
	public String saveFileRequest(String fileName, String formName)
	{
		System.out.print("KONDR: method saveFileRequest() must be implement in inherited class "+getClass());
		return null;
	}
	
	@Override
	public void init(ServletConfig conf) throws ServletException 
	{
		super.init(conf);
		config=conf;
		context=conf.getServletContext();
	}
	
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException 
	{
		request.setCharacterEncoding(characterEncodingIn);	
		response.setCharacterEncoding(characterEncodingOut);	
		response.setContentType(contentType);	
		
		try
		{
			HttpData http=new HttpData(request,response);
			httpGet(http);
			http.destroy();
		} 
		catch (SQLException e)
		{
			if (KContext.isDebug()) System.out.print(e.getMessage());
		}
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException 
	{
		request.setCharacterEncoding(characterEncodingIn);	
		response.setCharacterEncoding(characterEncodingOut);	
		response.setContentType(contentType);
		
		try
		{
			HttpData http=new HttpData(request,response);
			httpPost(http);
			http.destroy();
		} 
		catch (SQLException e)
		{
			if (KContext.isDebug()) System.out.print(e.getMessage());
		}
	}
	
	
	//*************************************************************************************
	//****************************** HttpData *********************************************
	//*************************************************************************************
	
	/**
	 * Содержит данные http запроса и ответа и методы их обработки
	 * @author kondr
	 */
	public class HttpData
	{
		final public HttpServletRequest request; 
		final public HttpServletResponse response;
		final private ServletOutputStream outStream;//Выходной поток для записи в него бинарных данных
		final private OutputStreamWriter writer;//Выходной потокок для записи в него текстовых данных в кодироке, установленной в сервлете
		private Cookie[] cookies;
		
		private int isMultipartFormData;// -1 - значение не определено, 0 - не Multipart, 1 - Multipart
		private String[] multipartParamNames;
		private String[] multipartParamValus;
		private int multipartParamSize;
						
		/**
		 * Создает
		 * @param req
		 * @param resp
		 * @throws IOException
		 */
		public HttpData(HttpServletRequest req, HttpServletResponse resp) throws IOException
		{
			request=req;
			response=resp;
			outStream= response.getOutputStream();
			writer=new OutputStreamWriter(outStream, characterEncodingOut);		
			cookies=null;
			
			multipartParamNames=new String[maxMultipartParams];
			multipartParamValus=new String[maxMultipartParams];
			multipartParamSize=0;
			
			//isMultipartFormData
			String ct=request.getHeader("content-type");
			if (ct==null) isMultipartFormData = 0;
			else isMultipartFormData = ct.indexOf("multipart/form-data;") >= 0 ? 1 : 0;
			
			//MultipartFormData
			if (isMultipartFormData == 1)
			{				
				MultipartParser parser = new MultipartParser(request, maxMultipartSizeMb * 1024 * 1024, true, true, characterEncodingIn);
				Part _part = null;
				while ((_part = parser.readNextPart()) != null) 
				{
					//Сохранение файлов
					if (_part.isFile())
					{
		                FilePart fPart = (FilePart) _part;
		                String fileName = fPart.getFileName();
		                String formName=fPart.getName();
		                
		                if (fileName != null && formName != null)
		                {
		                	String filePath=saveFileRequest(fileName,formName);
		                	if (filePath !=null && !filePath.isEmpty()) 
		                		fPart.writeTo(new java.io.File(filePath));
							multipartParamNames[multipartParamSize]=formName;
							multipartParamValus[multipartParamSize]=filePath;
		                }	                
					}
					//Сохранение параметров запроса
					else if (_part.isParam()) 
					{
						ParamPart pPart = (ParamPart) _part;
						multipartParamNames[multipartParamSize]=pPart.getName();
						multipartParamValus[multipartParamSize]=pPart.getStringValue(characterEncodingIn);
					}
					if (multipartParamSize++ >= maxMultipartParams) break;
				}
			}
			//no MultipartFormData
			else
			{
				Enumeration<String> es=request.getParameterNames();
				while(es.hasMoreElements()) 
				{
					String s=es.nextElement();
					multipartParamNames[multipartParamSize]=s;
					multipartParamValus[multipartParamSize]=request.getParameter(s);
					if (multipartParamSize++ >= maxMultipartParams) break;
				}
			}
		}
		
		public void destroy() throws IOException
		{
			writer.close();
			outStream.close();
		}
		
				
		//*************************** OutputStream & Writer ******************************************
		
		/**
		 * @return Выходной потокок для записи в него текстовых данных в кодироке, установленной в сервлете
		 */
		public OutputStreamWriter getWriter()
		{
			return writer;
		}
		
		/**
		 * @return Выходной поток для записи в него бинарных данных
		 */
		public ServletOutputStream getOutputStream()
		{
			return outStream;
		}
		
		/**
		 * Запись в выходной поток сервлета текстовых данных в установленной сервелетом кодировке
		 * @param value
		 * @throws IOException
		 */
		public void write(String value) throws IOException
		{
			writer.write(value);
		}	
		
		/**
		 * Записывает в выходной поток сервелета содержимое файла (картинки, текст и т.п.)
		 * при вставке из файла текста, файл должен быть в той же кодировке, что и выходной поток сервелета.
		 * @param fileName
		 * @throws IOException
		 */
		public void writeFromFile(String fileName) throws IOException
		{
			ServletUtils.returnFile(fileName, outStream);
		}	
		
		public void writeStringFromDB(String dbName, String sql) throws IOException 
		{
			writer.write(dba.getDbString(dbName, sql));
		}	
		
		public void writeTextFromDB(String dbName, String sql, String separator) throws IOException 
		{
			dba.writeDbText(dbName, sql, writer, separator);
		}		
		
	    public void writeJSArray(String dbName, String sql, String jsObjConstr) throws SQLException, IOException
	    {
	    	dba.writeJSArray(dbName, sql, writer, jsObjConstr);
	    }
	    
	    public void writeTemplate(KPageTemlate template, String[] inserts) throws IOException
	    {
	    	KPageTemlate.Iterator itr=template.getIterator();
	    	int idx=0;
	    	while(itr.next())
	    	{
	    		writer.write(itr.part());
	    		if (idx < inserts.length) writer.write(inserts[idx++]);
	    	}
	    }	    
		
		
		//*************************** Parameters ******************************************

		public String[] getParameterNames()
		{
			return multipartParamNames;
		}
		
		public int getParameterSize()
		{
			return multipartParamSize;
		}
		
		public String getParametr(String name)
		{
			for(int i=0;i<multipartParamSize;i++) if (multipartParamNames[i].equals(name)) return multipartParamValus[i];
			return "";
		}
		
		public String[] getUrlExtraParams()
		{
			String info=request.getPathInfo().substring(1);
			if (info!=null) return info.split("/");
			return null;
		}
		
				

		//*************************** Cookie ******************************************
		
		/**
		 * Получение Cookie. Если Cookie не существует - возвраается пустая строка.
		 * @param name Имя Cookie
		 * @return Значение Cookie
		 */
		public String getCookie(String name)
		{
			if (cookies==null) cookies=request.getCookies();
			for(Cookie c : cookies) if (c.getName()==name) return c.getValue();
			return "";
		}
		
		
		/**
		 * Устанговка ответного Cookie
		 * @param name Имя Cookie
		 * @param value Значение Cookie
		 */
		public void setCookie(String name, String value)
		{
			response.addCookie(new Cookie(name, value)); 
		}
		
		/**
		 * Устанговка ответного Cookie и времени его действия
		 * @param name Имя Cookie
		 * @param value Значение Cookie
		 */		
		public void setCookie(String name, String value, int expiryMin)
		{
			Cookie cook=new Cookie(name, value);
			cook.setMaxAge(expiryMin * 60);
			response.addCookie(cook); 
		}
		
		//*************************** Headers *********************************************
		
		/**
		 * Запись заголовка в http ответ
		 * @param name Имя заголовка
		 * @param value Значение заголовка
		 */
		public void setHeader(String name, String value)
		{
			response.setHeader(name, value);
		}
		
		/**
		 * Чтение заголовков http запроса
		 * @param name Имя заголовка
		 * @return Значение заголовка
		 */
		public String getHeader(String name)
		{
			return request.getHeader(name);
			
		}
		
		/**
		 * @return Referer
		 */
		public String getReferer()
		{
			return request.getHeader("referer");
		}
		
		/**
		 * Является ли запрос MultipartFormData
		 * @return true = MultipartFormData
		 */
		public boolean isMultipartFormData()
		{
			return isMultipartFormData == 1;
		}
			
		
		//*************************** Отладка ******************************************
		
		/**
		 * Вывод на системную консоль всех переданных сервлету параметров для не MultipartFormData запроса
		 */
		public void requestToConsole(boolean data,boolean params, boolean headers)
		{
			if (!KContext.isDebug()) return;
			
			System.out.print("\n\n*********** " + new Date().toString().substring(11,19) 
					+ " request " + request.getMethod() + " " +request.getRequestURI()+" ********************** \n\n");
					
			System.out.print("QueryString = "+request.getQueryString()+"\n");
			System.out.print("RemoteAddr: = "+request.getRemoteAddr()+"\n");
			
			System.out.print("\nПАРАМЕТРЫ ЗАПРОСА: \n");
			for(int i=0;i<multipartParamSize;i++) System.out.print(i+". "+multipartParamNames[i]+" = "+multipartParamValus[i]+"\n");
			
			System.out.print("\nЗАГОЛОВКИ ЗАПРОСА:\n");
			Enumeration<String> hdrs=request.getHeaderNames();
			while (hdrs.hasMoreElements())
			{
				String n=hdrs.nextElement();
				System.out.print(n+" = "+request.getHeader(n)+"\n");
			}
		}
		
		public void writeTestForm() throws IOException
		{
			writer.write("<div class='testForm'><form  method='post'>"+
						"<input name=\"text1\" type=\"text\" />"+
						"<input type=\"submit\" value=\"send\" /></form></div>");
		}
		
		public void writeTestFormMultipart() throws IOException
		{
			writer.write("<div class='testForm'><form  method='post' enctype='multipart/form-data'>"+
					"<input name=\"text1\" type=\"text\" />"+
					"<input name=\"file1\"  type=\"file\" value=\"File...\" />"+
					"<input type=\"submit\" value=\"send multipart\" /></form></div>");
		}		
	}
	
}
