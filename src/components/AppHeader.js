import React from 'react';
import { makeStyles } from '@material-ui/styles';
import AppBar from '@material-ui/core/AppBar';
import IconButton from '@material-ui/core/IconButton';
import Menu from '@material-ui/core/Menu';
import MenuIcon from '@material-ui/icons/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(() => ({
  title: {
    flexGrow: 1,
    textAlign: 'center',
  },
  appHeader: {
    color: '#e2e2e2',
    backgroundColor: '#0066e2',
  },
  appFooter: {
    color: '#e2e2e2',
    backgroundColor: '#0066e2',
    top: 'auto',
    bottom: 0,
  },
  menuLink: {
    width: 'auto',
    overflow: 'hidden',
    fontSize: '1rem',
    boxSizing: 'border-box',
    minHeight: '48px',
    fontFamily: "Acme",
    fontWeight: '400',
    lineHeight: '1.5',
    paddingTop: '6px',
    whiteSpace: 'nowrap',
    letterSpacing: '0.00938em',
    paddingBottom: '6px',
    textDecoration: 'none',
  },
}));

const ITEM_HEIGHT = 48;

const options = [
  // {label: 'Authors', url: '/#/authors/'},
  {label: 'Books', url: '/#/books/'},
  {label: 'Statistics', url: '/#/stats/'},
];

export const AppHeader = () => {
  const classes = useStyles();

  const [anchorEl, setAnchorEl] = React.useState();
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handlePageChange = (url) => {
    return () => {
      window.location = url;
    }
  }

  return (
    <AppBar position="static" className={classes.appHeader}>
      <Toolbar>
       <IconButton
          edge="start"
          className={classes.menuButton}
          color="inherit"
          aria-label="menu"
          onClick={handleClick}
        >
          <MenuIcon />
        </IconButton>
        <Menu
            id="long-menu"
            MenuListProps={{
              'aria-labelledby': 'long-button',
            }}
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
            PaperProps={{
              style: {
                maxHeight: ITEM_HEIGHT * 4.5,
                width: '20ch',
              },
            }}
          >
            {options.map((option) => (
              <MenuItem key={option.label} selected={option.label === 'Authors'} onClick={handleClose}>
              <div onClick={handlePageChange(option.url)}>
                {option.label}
              </div>
              </MenuItem>
            ))}
          </Menu>
        <Typography variant="h6" className={classes.title}>
          Jessica's Reading Nook
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export const AppFooter = () => {
  const classes = useStyles();

  return (
    <AppBar position="fixed" color="primary" className={classes.appFooter}>
      <p>Footer</p>
    </AppBar>
  );
};
