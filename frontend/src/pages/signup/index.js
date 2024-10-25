import { Container, Input, Title, Main, Form, Button } from '../../components'
import styles from './styles.module.css'
import { useFormWithValidation } from '../../utils'
import { Redirect } from 'react-router-dom'
import { useContext, useState } from 'react'
import { AuthContext } from '../../contexts'
import MetaTags from 'react-meta-tags'

const SignUp = ({ onSignUp }) => {
  const { values, handleChange, isValid, errors } = useFormWithValidation()
  const authContext = useContext(AuthContext)

  const handleSubmit = (e) => {
    e.preventDefault()

    // Проверяем, все ли поля валидны
    if (!isValid) {
      return
    }

    // Если пароли совпадают, вызываем функцию регистрации
    onSignUp(values)
  }

  return (
    <Main>
      {authContext && <Redirect to='/recipes' />}
      <Container>
        <MetaTags>
          <title>Регистрация</title>
          <meta name="description" content="Хакатон - Регистрация" />
          <meta property="og:title" content="Регистрация" />
        </MetaTags>
        <Title title='Регистрация' />
        <Form className={styles.form} onSubmit={handleSubmit}>
          <Input
            label='ФИО'
            name='fio'
            required
            onChange={handleChange}
            error={errors.name} // Отображаем ошибку, если есть
          />
          <Input
            label='Логин'
            name='username'
            required
            onChange={handleChange}
            error={errors.username} // Отображаем ошибку, если есть
          />
          <Input
            label='Пароль'
            type='password'
            name='password'
            required
            onChange={handleChange}
            error={errors.password} // Отображаем ошибку, если есть
          />
          <Input
            label='Повтор пароля'
            type='password'
            name='password_re'
            required
            onChange={handleChange}
            error={errors.password_re} // Отображаем ошибку, если есть
          />
          <Button
            modifier='style_dark-blue'
            type='submit'
            className={styles.button}
            disabled={!isValid || values.password !== values.password_re}
          >
            Зарегистрироваться
          </Button>
        </Form>
      </Container>
    </Main>
  )
}

export default SignUp
