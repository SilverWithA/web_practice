package com.example.springSignup;

import com.example.springSignup.User.SignUp;
import com.example.springSignup.User.SignUpRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Optional;

@SpringBootTest
public class SignUpRepositoryTest {

    @Autowired
    private SignUpRepository signUpRepository;

    @Test
    void testJpa(){
        SignUp user1 = new SignUp();
        user1.setUsername("사람1");
        user1.setPassword("사람사람111");
        user1.setEmail("person1@email.com");
        this.signUpRepository.save(user1);

        SignUp user2 = new SignUp();
        user2.setUsername("사람2");
        user2.setPassword("사람사람222");
        user2.setEmail("person22@email.com");
        this.signUpRepository.save(user2);
    }

    @Test
    void testJpa1(){
        Optional<SignUp> up = this.signUpRepository.findByUsername("사람사람111");
        if(up.isPresent()){
            SignUp user = up.get();
            Assertions.assertEquals(1,user.getId());
        }
    }
}
