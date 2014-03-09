package kondr.KServlet;

import java.security.MessageDigest;

public class KEncoder
{
	private static final String base64code = 
			"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
 
	public static String encodeBase64(byte[] array)
	{
		int i=0;
		int eq=0;
		int size=array.length;
		StringBuilder sb=new StringBuilder(size*2);
		while(i < size)
		{
			int b3 = (array[i] & 0xff) << 16;
			if (++i < size) b3 |= (array[i] & 0xff) << 8; else eq++;		
			if (++i < size) b3 |= (array[i] & 0xff); else eq++;		
			i++;
			
			sb.append(base64code.charAt((b3 >>> 18) & 0x3f));
			sb.append(base64code.charAt((b3 >>> 12) & 0x3f));
			sb.append(eq>1?'=':base64code.charAt((b3 >>> 6) & 0x3f));
			sb.append(eq>0?'=':base64code.charAt(b3 & 0x3f));
		}
		return sb.toString();
	}
	
	public static byte[] MD5(String value)
	{
        try
        {
        	MessageDigest md5 = MessageDigest.getInstance("MD5");
        	return md5.digest(value.getBytes());
        }
        catch (Exception e){throw new RuntimeException(e);}
	}
	
	public static String MD5Base64(String value)
	{
        try
        {
        	MessageDigest md5 = MessageDigest.getInstance("MD5");
        	return encodeBase64(md5.digest(value.getBytes()));
        }
        catch (Exception e){throw new RuntimeException(e);}
	}
	
	public static byte[] SHA1(String value)
	{
        try
        {
        	MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
        	return sha1.digest(value.getBytes());
        }
        catch (Exception e){throw new RuntimeException(e);}
	}
	
	public static String SHA1Base64(String value)
	{
        try
        {
        	MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
        	return encodeBase64(sha1.digest(value.getBytes()));
        }
        catch (Exception e){throw new RuntimeException(e);}
	}
	
}
