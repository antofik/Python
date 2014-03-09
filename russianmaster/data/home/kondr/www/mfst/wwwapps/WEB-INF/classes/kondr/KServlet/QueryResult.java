package kondr.KServlet;

import org.apache.tomcat.jdbc.pool.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Результат SQL запроса
 * Используя подключение из пула, создает и выполняет SQL команду
 */
public class QueryResult
{
	private Connection con=null;
	private Statement st=null;
	private ResultSet rs=null;	
	
	public QueryResult(DataSource pool,String sql) throws SQLException
	{
		//System.out.print("\n\n QueryResult - create \n\n");
		try
		{
			con=pool.getConnection();
			st=con.createStatement();
			rs=st.executeQuery(sql);
		} 
		catch (SQLException e)
		{
			if (rs!=null) try{rs.close();}catch (SQLException ex) {System.out.print("KONDR QueryResult creating error (1) " + ex.getMessage());}
			if (st!=null) try{st.close();}catch (SQLException ex) {System.out.print("KONDR QueryResult creating error (2) " + ex.getMessage());}
			if (con!=null) try{con.close();}catch (SQLException ex) {System.out.print("KONDR QueryResult creating error (3) " + ex.getMessage());}
			System.out.print("KONDR QueryResult creating error (4) " + e.getMessage());
			throw e;
		}
	}
	
	public ResultSet getResultSet()
	{
		return rs;
	}
	
	public void close() 
	{
        try
		{
		  rs.close();
          st.close();
          con.close();
		} 
        catch (SQLException e)
		{
			e.printStackTrace();
		}
        //System.out.print("\n\n QueryResult - close \n\n");
	}
}
