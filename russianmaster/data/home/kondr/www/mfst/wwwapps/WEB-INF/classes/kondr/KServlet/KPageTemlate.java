package kondr.KServlet;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

public class KPageTemlate
{
	String startTag;
	String endTag;
	int startTagLen;
	int endTagLen;
	String templateParts[];
	String templateVars[];
	

	public KPageTemlate()
	{
		startTag="<!--";
		startTagLen=startTag.length();
		
		endTag="-->";
		endTagLen=endTag.length();
		
	}
	public KPageTemlate(String startTag, String endTag)
	{
		this.startTag=startTag;
		this.startTagLen=startTag.length();
		
		this.endTag=endTag;
		this.endTagLen=endTag.length();
	}
	
	/**
	 * Подготаввливаем шаблон - нарезаем строки, для последующего соединения
	 * @param fileName
	 */
	public void prepare(String fileName, String charSet) 
	{
		FileInputStream stream=null;
		try
		{
			/// !!! stream.available() - стремный код - нужно усовершенствовать чтение из файла с троку
			stream = new FileInputStream(fileName);
			byte[] fileData = new byte[stream.available()];
			stream.read(fileData);
			String source=new String(fileData, charSet);
			
			
			int count=0;
			int startTagIdx=0;
			while((startTagIdx=source.indexOf(startTag, startTagIdx+1)) > 0) count++;
			templateParts= new String[count+1];
			templateVars = new String[count];
			
			startTagIdx=0;
			count=0;
			int preIdx=0;
			while((startTagIdx=source.indexOf(startTag, startTagIdx+1)) > 0)
			{
				int endTagIdx=source.indexOf(endTag, startTagIdx+1);
				if (endTagIdx<0) {System.out.print("\n******** no endTagIdx **********\n");return;}
				
				templateParts[count]=source.substring(preIdx, startTagIdx);
				templateVars[count]=source.substring(startTagIdx+startTagLen, endTagIdx);
				
				preIdx=endTagIdx+endTagLen;
				count++;
			}
			if(preIdx < source.length()) templateParts[count]=source.substring(preIdx);
			else templateParts[count]="";
		} 
		catch (UnsupportedEncodingException e){System.out.print("KPageTemlate.prepare() -> Unsupported Encoding Exception ");e.printStackTrace();} 
		catch (FileNotFoundException e){System.out.print("KPageTemlate.prepare() -> File Not Found: "+fileName);e.printStackTrace();}
		catch (IOException e){System.out.print("KPageTemlate.prepare() -> IOException. File: "+fileName);e.printStackTrace();}
		finally
		{
			//if (fc != null)	try{fc.close();} catch (IOException e){e.printStackTrace();}
			if (stream != null)	try{stream.close();} catch (IOException e){e.printStackTrace();}
		}
	}
	
	public int partLength()
	{
		return templateParts.length;
	}
	
	public String getPart(int index)
	{
		if (index < templateParts.length) return templateParts[index];
		else return "";
	}
	
	public String getParamName(int index)
	{
		if (index < templateVars.length) return templateVars[index];
		else return "";
	}
	
	public Iterator getIterator()
	{
		return new Iterator();
	}
	
	public class Iterator
	{
		int curIdx;
		int templatePartsLength;
		public Iterator()
		{
			curIdx=-1;
			templatePartsLength=KPageTemlate.this.templateParts.length;
		}
		
		public boolean next()
		{
			curIdx++;
			return curIdx < templatePartsLength;
		}
		
		public String part()
		{
			if (curIdx < templatePartsLength) return KPageTemlate.this.templateParts[curIdx];
			else return "";
		}	
		
		public String ParamName()
		{
			if (curIdx < templatePartsLength-1) return KPageTemlate.this.templateVars[curIdx];
			else return "";
		}		
		
	}
	
}
