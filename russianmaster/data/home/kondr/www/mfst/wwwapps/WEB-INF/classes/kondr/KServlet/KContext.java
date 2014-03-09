package kondr.KServlet;

import java.util.*;
import javax.servlet.*;
import javax.servlet.annotation.*;

/**
 * Создаем статический объект для доступа к базе данных
 */
@WebListener
public class KContext implements ServletContextListener {

	final private static String dbParamPrefix="dataBase-";
	public static DbAccess dba;
	private static boolean debug;

    public static boolean isDebug()
	{
		return debug;
	}

	public KContext() {}

    public void contextInitialized(ServletContextEvent sce) 
    {	
    	ServletContext sc=sce.getServletContext();
    	
    	debug = sc.getInitParameter("debug")!=null;
     	if (debug) System.out.print(" ****************** Klistener() contextInitialized ****************** \n");
   	
    	//Создание пулов подключений к базамм данных
    	List<String> dbNames= new ArrayList<String>();
    	Enumeration<String> prms=sc.getInitParameterNames();
    	while(prms.hasMoreElements())
    	{
    		String prmName=prms.nextElement();
    		if (prmName.indexOf(dbParamPrefix)==0) dbNames.add(prmName.substring(dbParamPrefix.length()));
    	}
    	dba = new DbAccess(dbNames.size());
    	for(String dbName : dbNames) dba.addPool(dbName, sc.getInitParameter(dbParamPrefix+dbName));
    }

    public void contextDestroyed(ServletContextEvent sce) 
    {
    	dba.destroy();
    	if (debug) System.out.print(" ****************** Klistener() contextDestroyed ****************** \n");
    }	
}

