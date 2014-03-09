package kondr.dance;

import java.util.HashMap;


public class RegData
{
	
	HashMap<Integer,String> men,women,area;
	String	treiners,clubs,countries; 

	public RegData()
	{
		men=new HashMap<Integer,String>(100);
		women=new HashMap<Integer,String>(100);
		area=new HashMap<Integer,String>(100);
	}
	
	public void refreshData()
	{
		men.clear();
		women.clear();
		area.clear();
		
		men.put(1050,"CB.Men['К']=[{r:'КАвстралия',e:'Australia'},{r:'КАлбания',e:'Albania'}];");
	}
	
	public String getMen(int key)
	{
		return men.containsKey(key) ? men.get(key) : "";
	}
	
	public String getWomen(int key)
	{
		return women.containsKey(key) ? women.get(key) : "";
	}
	
	public String getArea(int key)
	{
		return area.containsKey(key) ? area.get(key) : "";
	}
	
	
	public String getTreiner()
	{
		return treiners.isEmpty() ? "" : treiners;
	}
	
	public String getClub()
	{
		return clubs.isEmpty() ? "" : clubs;
	}
	
	public String getCountry()
	{
		return countries.isEmpty() ? "" : countries;
	}
}
