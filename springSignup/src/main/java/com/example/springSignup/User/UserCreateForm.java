package com.example.springSignup.User;

import lombok.Getter;
import lombok.Setter;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Size;


@Getter
@Setter
public class UserCreateForm {
    @Size(min=3, max=20)
    @NotEmpty(message = "사용자 ID를 입력하세요!")
    private String username;

    @NotEmpty(message = "비밀번호를 입력하세요!")
    private String password1;
    @NotEmpty(message = "비밀번호는 확인을 입력하세요!")
    private String password2;

    //@Email은 이메일 형식인지 확인해주는 어노테이션
    @Email
    @NotEmpty(message = "이메일을 입력해주세요")
    private String email;
}
