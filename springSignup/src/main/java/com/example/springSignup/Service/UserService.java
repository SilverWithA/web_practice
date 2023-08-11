package com.example.springSignup.Service;

import com.example.springSignup.User.SignUpRepository;
import com.example.springSignup.User.SignUp;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private final SignUpRepository signUpRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(SignUpRepository signUpRepository,PasswordEncoder passwordEncoder){
        this.signUpRepository = signUpRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public SignUp create(String username, String email, String password){
        SignUp user = new SignUp();
        user.setUsername(username);
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(password));
        this.signUpRepository.save(user);
        return user;
    }

}
