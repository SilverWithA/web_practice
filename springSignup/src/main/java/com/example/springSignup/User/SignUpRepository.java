package com.example.springSignup.User;

import com.example.springSignup.User.SignUp;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SignUpRepository extends JpaRepository<SignUp,Long> {

    Optional<SignUp> findByUsername(String username);

}
