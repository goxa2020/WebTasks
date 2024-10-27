import styles from './style.module.css'
import cn from 'classnames'
import { LinkComponent } from '../index'
import navigation from '../../configs/navigation'

const Nav = ({ loggedIn, orders }) => {
  return <nav className={styles.nav}>
    <div className={styles.nav__container}>
      <div className={styles.filtercontainer}>
        <div className={styles.icont}>
        <i className={"fa fa-filter"} aria-hidden="true"></i>
        <div className={styles.del}>|</div>
        </div>
      <input type="text" id="name" name="name"/>
      </div>
      <ul className={styles.nav__items}>
        {navigation.map(item => {
          if (!loggedIn && item.auth) { return null }
          return <li className={cn(styles.nav__item, {
            [styles.nav__item_active]: false
          })} key={item.href}>
            <LinkComponent
              title={item.title}
              activeClassName={styles.nav__link_active}
              href={item.href}
              exact
              className={styles.nav__link}
            />
            {item.href === '/cart' && orders > 0 && <span className={styles['orders-count']}>{orders}</span>}
          </li>
        })}
      </ul>
    </div>
  </nav>
}

export default Nav
