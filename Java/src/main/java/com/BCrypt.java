package ecinema;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.bcrypt.BCrypt;
import java.lang.Object;

public class BCrypt extends java.lang.Object {

    public BCrypt(String pass);
    {
	String pw_hash = BCrypt.hashpw(pass, BCrypt.gensalt());
	
    }//BCrypt

}//BCrypt