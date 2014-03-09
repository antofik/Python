package kondr.KServlet;

import java.io.IOException;
import java.sql.SQLException;

import java.util.ArrayList;
//import java.util.Date;
import java.util.List;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;

import javax.imageio.ImageIO;

import java.awt.Color;
import java.awt.Font;

import nl.captcha.Captcha;
import nl.captcha.backgrounds.GradiatedBackgroundProducer;
import nl.captcha.text.renderer.DefaultWordRenderer;
import nl.captcha.noise.StraightLineNoiseProducer;
//import nl.captcha.noise.CurvedLineNoiseProducer;

public class KCapture extends KServlet
{
	
    private static int _width = 155;
    private static int _height = 50;
    
    private static final List<Color> COLORS = new ArrayList<Color>(2);
    private static final List<Font> FONTS = new ArrayList<Font>(3);
    
    static {
        COLORS.add(new Color(0,0,0));
        COLORS.add(new Color(255,255,255));
        COLORS.add(new Color(228,167,167));
        COLORS.add(new Color(118,216,237));
        COLORS.add(new Color(239,221,97));
        COLORS.add(new Color(219,107,228));
        COLORS.add(new Color(118,218,123));
        COLORS.add(new Color(168,255,238));
        COLORS.add(new Color(202,198,255));
        COLORS.add(new Color(254,255,198));
        COLORS.add(new Color(158,24,24));
        COLORS.add(new Color(159,158,163));
        COLORS.add(new Color(185,122,199));
        COLORS.add(new Color(71,213,47));
        COLORS.add(new Color(70,159,189));

        
        
        FONTS.add(new Font("Geneva", Font.ITALIC, 48));
        FONTS.add(new Font("Courier", Font.BOLD, 48));
        FONTS.add(new Font("Arial", Font.BOLD, 48));
    }
    
	@Override
	public void init(ServletConfig conf) throws ServletException 
	{
		super.init(conf);
		contentType="image/png";
	}

	@Override
	public void httpGet(HttpData http) throws SQLException,
			ServletException, IOException
	{
		DefaultWordRenderer wordRenderer = new DefaultWordRenderer(COLORS, FONTS);
        Captcha captcha = new Captcha.Builder(_width, _height)
        		.addText(wordRenderer)
                .gimp() 
                .addNoise(new StraightLineNoiseProducer(new Color(47,74,163), 3))                
                .addNoise(new StraightLineNoiseProducer(new Color(139,209,138), 3))                
                .addNoise(new StraightLineNoiseProducer(new Color(47,74,163), 3))                
                .addNoise(new StraightLineNoiseProducer(new Color(139,209,138), 3))                
                .addBackground(new GradiatedBackgroundProducer(new Color(0,4,176),new Color(170,255,130)))
                .build();
        
        String code=KEncoder.SHA1Base64(captcha.getAnswer());
        http.setCookie("cpt", code);
        http.setHeader(RsH_CacheControl, "private,no-cache,no-store");
        
        //System.out.print("\n\n** captcha.getAnswer = "+captcha.getAnswer()+"\n"+code);       
       
        ImageIO.write(captcha.getImage(), "png", http.getOutputStream());        
	}

	@Override
	public void httpPost(HttpData http) throws SQLException,
			ServletException, IOException
	{
		// TODO Auto-generated method stub

	}

}

