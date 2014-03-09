
package kondr.KServlet;

import org.apache.tomcat.jdbc.pool.DataSource;
import org.apache.tomcat.jdbc.pool.PoolProperties;


import java.io.IOException;
import java.io.OutputStreamWriter;
import java.sql.*;

/**
 * Управление подключениями к базам данных.
 * Создает пул подключения для каждой базы
 * Выполняет простые запросы к базам данных
 */
public class DbAccess
{
	/**
	 * Обеспечиавает доступ к пулам подключений по имени
	 */
	static private class PoolMap
	{
		DataSource pools[];
		String names[];
		int size;
		
		public PoolMap(int Capacity)
		{
			pools = new DataSource[Capacity];
			names = new String[Capacity];
			size=0;
		}
		
		public void add(String name, DataSource pool)
		{
			names[size]=name;
			pools[size]=pool;
			size++;
		}
		
		public DataSource at(String name)
		{
			for(int i=0;i<size;i++) if (names[i].equals(name)) return  pools[i];
			return null;
		}
		
		public void destroy()
		{
			for(int i=0;i<size;i++) pools[i].close();
		}
	}
	
	PoolMap pools;
	
	/**
	 * @param Capacity Число баз данных, к которым потребуется доступ
	 */
	public DbAccess(int Capacity)
	{
		pools = new PoolMap(Capacity);
	}
	
	/**
	 * Создает пул подключений к базе данных
	 * @param dbName Имя база данных
	 * @param dbConnString Строка подключения к базе данных: host:port/dbname;login;password
	 */
	public void addPool(String dbName, String dbConnString)
	{
		String dbConnData[]=dbConnString.split(";");
		if (dbConnData.length<3) throw new RuntimeException("DbAccess: invalid dbConnString = " + dbConnString);
		
		PoolProperties p = new PoolProperties();
        p.setUrl("jdbc:mysql://"+dbConnData[0]);
        p.setDriverClassName("com.mysql.jdbc.Driver");
        p.setUsername(dbConnData[1]);
        p.setPassword(dbConnData[2]);
        p.setJmxEnabled(true);
        p.setTestWhileIdle(false);
        p.setTestOnBorrow(true);
        p.setValidationQuery("SELECT 1");
        p.setTestOnReturn(false);
        p.setValidationInterval(30000);
        p.setTimeBetweenEvictionRunsMillis(30000);
        p.setMaxActive(30);
        p.setInitialSize(5);
        p.setMaxWait(10000);
        p.setMaxIdle(20);
        p.setRemoveAbandonedTimeout(60);
        p.setMinEvictableIdleTimeMillis(30000);
        p.setMinIdle(10);
        p.setLogAbandoned(true);
        p.setRemoveAbandoned(true);
        p.setJdbcInterceptors("org.apache.tomcat.jdbc.pool.interceptor.ConnectionState;org.apache.tomcat.jdbc.pool.interceptor.StatementFinalizer");
        
        DataSource pool = new DataSource();
        pool.setPoolProperties(p);
        pools.add(dbName, pool);
	}
	
	public void destroy()
	{
		pools.destroy();
	}
    
    /**
     * Выполняет в указанной базе SQL запрос на выборку
     * После чтения данных следует закрыть возвращенный объект
     * @param dbName
     * @param sql
     * @return 
     */
    QueryResult executeQuery(String dbName, String sql) throws SQLException 
    {
    	return new QueryResult(pools.at(dbName), sql);
    }
    /**
     * Выполняет sql запрос, который должен возвращать список строковых значений
     * и записывает результат в выходной поток
     * @param dbName имя базы данных
     * @param sql - запрос
     * @param writer - выходной поток
     * @param separator - разделитель строковых значений
     */
    public void writeDbText(String dbName, String sql, OutputStreamWriter writer, String separator) throws IOException 
	{
    	boolean isFirst=true;
    	QueryResult qr=null;
    	try
		{
			qr=new QueryResult(pools.at(dbName),sql);
			ResultSet rs=qr.getResultSet();
			while(rs.next())
			{
				if (isFirst) isFirst=false;
				else writer.write(separator);
				writer.write(rs.getString(1));
			}
		} 
    	catch (SQLException e){e.printStackTrace();}
    	finally{if (qr!=null) qr.close();}
	} 
    
    /**
     * Преобразует sql запрос в JavaScript массив, состоящий из конструкторов объектов:<br/>
     * [new jsObjConstr(...), ... new jsObjConstr(...)];
     * @param dbName Имя базы данных
     * @param sql Запрос на выборку
     * @param OutputStreamWriter writer
     * @param jsСonstr функция-конструктор объектов;
     */
    public void writeJSArray(String dbName, String sql, OutputStreamWriter writer, String jsСonstr) throws SQLException, IOException
	{
    	boolean isFirst=true;
       
		QueryResult qr = new QueryResult(pools.at(dbName), sql);
        ResultSet rs=qr.getResultSet();
        
        //Тип данных в колонках таблицы
        ResultSetMetaData md=rs.getMetaData();
        int columns=md.getColumnCount();
        boolean isNum[]=new boolean[columns+1];
        for(int i=1;i<=columns;i++) 
    	{
        	String cls=md.getColumnClassName(i);
        	isNum[i] = cls.equals("java.lang.Long") || cls.equals("java.lang.Integer") || cls.equals("java.math.BigInteger") 
        			|| cls.equals("java.lang.Short") || cls.equals("java.lang.Byte") || cls.equals("java.lang.Boolean");
    	}
        writer.write("[\n");
 		while (rs.next()) 
		{
 			if (isFirst) isFirst=false;
 			else writer.write(",\n");
 			writer.write("new "+jsСonstr+"(");
			for(int i=1;i<=columns;i++)
			{
				if (isNum[i]) writer.write(rs.getObject(i).toString());
				else writer.write("'"+rs.getObject(i).toString()+"'");
				
				if (i!=columns) writer.write(",");
			}
			writer.write(")");
		}
 		writer.write("\n];");
 		
		qr.close();
	}

        
    /**
     * Используется для получения из БД одной строки данных 
     * @param sql Запрос, который должен возвращать единственную строку с одним столбцом.
     * @return Строковое значение первой строки первого столбца.
     */
    public String getDbString(String dbName, String sql) 
	{
    	QueryResult qr=null;
    	try
		{
			qr=new QueryResult(pools.at(dbName),sql);
			ResultSet rs=qr.getResultSet();
			if (rs.next()) return rs.getString(1);
		} 
    	catch (SQLException e){if (qr!=null) qr.close(); e.printStackTrace();}
    	finally{if (qr!=null) qr.close();}
    	   	
		return "";
	} 
    
    /**
     * Получения одного объекта из базы данных. Затем объект должен быть приведен к нужному типу. 
     * @param sql Запрос, который должен возвращать единственную строку с одним столбцом.
     * @return Значение первой строки первого столбца.
     */
    public Object getDbObject(String dbName, String sql)
	{
    	QueryResult qr=null;
    	try
		{
			qr=new QueryResult(pools.at(dbName),sql);
			ResultSet rs=qr.getResultSet();
			if (rs.next()) return rs.getObject(1);
		} 
    	catch (SQLException e){if (qr!=null) qr.close(); e.printStackTrace();}
    	finally{if (qr!=null) qr.close();}
    	
		return null;
	} 
    
    /**
     * Получения целого значения из базы данных.  
     * @param sql Запрос, который должен возвращать единственную строку с одним столбцом.
     * @param defValue Значение, которое ыдет возвращено в случае отсутствия в таблице требуемых данных
     * @return Значение первой строки первого столбца.
     */
    public int getDbInt(String dbName, String sql, int defValue)
	{
    	QueryResult qr=null;
    	try
		{
			qr=new QueryResult(pools.at(dbName),sql);
			ResultSet rs=qr.getResultSet();
			if (rs.next()) return rs.getInt(1);
		} 
    	catch (SQLException e){e.printStackTrace(); if (qr!=null) qr.close(); }
    	finally{if (qr!=null) qr.close();}
    	
		return defValue;
	}
    
    /**
     * Проверка существования строки в базе данных.  
     * @param sql Запрос, который должен возвращать единственную строку.
     * @param defValue Значение, которое ыдет возвращено в случае отсутствия в таблице требуемых данных
     * @return true, если строка существует.
     */
    public boolean isDbExists(String dbName, String sql) 
	{
    	QueryResult qr=null;
    	try
		{
			qr=new QueryResult(pools.at(dbName),sql);
			ResultSet rs=qr.getResultSet();
			return rs.next();
		} 
    	catch (SQLException e){e.printStackTrace();if (qr!=null) qr.close(); }
    	finally{if (qr!=null) qr.close();}
    	return false;
	}
}

