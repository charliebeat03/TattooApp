from kivy.app import App
from kivy.core.window import Window
import os
import sys
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from supabase import create_client
import webbrowser

# Configuración Supabase
SUPABASE_URL = "https://kgptrbtxyqcfcxmpunso.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtncHRyYnR4eXFjZmN4bXB1bnNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1Mzc3ODcsImV4cCI6MjA3NTExMzc4N30.G4ILYZdW8WGQkhSaDZFjXfj1zLkO1YS_WjGLI4_aQKM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class CustomNavigationDrawer(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = (0, 16, 16, 0)

class LoginScreen(Screen):
    def verificar_login(self, usuario, password):
        try:
            user = supabase.auth.sign_in_with_password({
                "email": usuario,
                "password": password
            })
            
            perfil = supabase.table("profiles").select("role").eq("id", user.user.id).execute()
            
            if perfil.data[0]['role'] == 'admin':
                self.manager.current = 'admin'
            else:
                self.manager.current = 'catalogo'
                
        except Exception as e:
            print("Error login:", e)
            self.mostrar_error("Error en login: Verifica tus credenciales")

    def mostrar_error(self, mensaje):
        dialog = MDDialog(
            title="Error de Autenticación",
            text=mensaje,
            size_hint=(0.8, 0.3)
        )
        dialog.open()

class CatalogoScreen(Screen):
    search_input = ObjectProperty(None)
    
    def clear_hint(self, instance, value):
        """Limpia el hint_text cuando el campo gana foco"""
        if value:  # Si gana foco
            instance.hint_text = ""
        else:      # Si pierde foco
            if instance.text == "":
                instance.hint_text = "Buscar tatuajes por nombre..."

    def on_enter(self):
        self.cargar_tatuajes()
    
    def cargar_tatuajes(self, search_text=""):
        try:
            response = supabase.table("catalogos").select("*, categorias(nombre)").execute()
            tatuajes = response.data
            
            if search_text:
                tatuajes = [t for t in tatuajes if search_text.lower() in t['nombre_estilo'].lower()]
            
            grid = self.ids.grid_tatuajes
            grid.clear_widgets()
            
            for tatuaje in tatuajes:
                self.agregar_tatuaje_grid(tatuaje)
                
        except Exception as e:
            print("Error cargando tatuajes:", e)
    
    def agregar_tatuaje_grid(self, tatuaje):
        grid = self.ids.grid_tatuajes
        
        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=("280dp", "380dp"),
            padding="12dp",
            spacing="8dp",
            elevation=8,
            radius=[20],
            md_bg_color=(1, 1, 1, 0.95)
        )
        
        imagen = AsyncImage(
            source=tatuaje['url_imagen'],
            size_hint_y=0.6,
            allow_stretch=True,
            keep_ratio=True,
            fit_mode="cover"
        )
        card.add_widget(imagen)
        
        info_box = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing="5dp")
        
        nombre = Label(
            text=tatuaje['nombre_estilo'],
            size_hint_y=0.3,
            text_size=(250, None),
            color=(0.1, 0.1, 0.1, 1),
            bold=True,
            font_size='16sp'
        )
        info_box.add_widget(nombre)
        
        categoria = Label(
            text=f"Categoria: {tatuaje['categorias']['nombre']}",
            size_hint_y=0.2,
            text_size=(250, None),
            color=(0.4, 0.4, 0.4, 1),
            font_size='12sp'
        )
        info_box.add_widget(categoria)
        
        precio_text = f"Precio: {tatuaje['precio_cup']} CUP"
        precio_color = (0.9, 0.1, 0.1, 1)  # Rojo para ofertas
        
        if tatuaje['tiene_descuento']:
            precio_text = f"OFERTA: {tatuaje['precio_descuento']} CUP"
            precio_color = (0.2, 0.6, 0.2, 1)  # Verde para ofertas
        
        label_precio = Label(
            text=precio_text,
            size_hint_y=0.25,
            text_size=(250, None),
            color=precio_color,
            bold=True,
            font_size='14sp'
        )
        info_box.add_widget(label_precio)
        
        btn_whatsapp = MDRaisedButton(
            text="Solicitar por WhatsApp",
            size_hint_y=0.4,
            md_bg_color=(0.12, 0.65, 0.34, 1),
            font_size='13sp'
        )
        btn_whatsapp.bind(on_release=lambda x: self.contactar_whatsapp(tatuaje))
        info_box.add_widget(btn_whatsapp)
        
        card.add_widget(info_box)
        grid.add_widget(card)
    
    def contactar_whatsapp(self, tatuaje):
        numero = "+5355549887"
        mensaje = f"Hola! Me interesa el tatuaje: {tatuaje['nombre_estilo']}. Precio: {tatuaje['precio_cup']} CUP"
        if tatuaje['tiene_descuento']:
            mensaje += f" (EN OFERTA: {tatuaje['precio_descuento']} CUP)"
        url_whatsapp = f"https://wa.me/{numero}?text={mensaje}"
        webbrowser.open(url_whatsapp)
    
    def buscar_tatuajes(self):
        search_text = self.ids.search_input.text
        self.cargar_tatuajes(search_text)
    
    def toggle_nav_drawer(self):
        nav_drawer = self.ids.nav_drawer
        if nav_drawer.state == 'open':
            nav_drawer.set_state('close')
        else:
            nav_drawer.set_state('open')

class AdminScreen(Screen):
    def on_enter(self):
        self.cargar_tatuajes_admin()
        self.cargar_categorias()
    
    def cargar_tatuajes_admin(self):
        try:
            response = supabase.table("catalogos").select("*, categorias(nombre)").execute()
            tatuajes = response.data
            
            grid = self.ids.grid_admin_tatuajes
            grid.clear_widgets()
            
            for tatuaje in tatuajes:
                self.agregar_tatuaje_admin_grid(tatuaje)
                
        except Exception as e:
            print("Error cargando tatuajes admin:", e)
    
    def agregar_tatuaje_admin_grid(self, tatuaje):
        grid = self.ids.grid_admin_tatuajes
        
        card = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            height="80dp",
            padding="15dp",
            spacing="15dp",
            elevation=4,
            radius=[12]
        )
        
        info_layout = BoxLayout(orientation='vertical')
        nombre_label = Label(
            text=tatuaje['nombre_estilo'],
            size_hint_y=0.5,
            text_size=(200, None),
            color=(0.1, 0.1, 0.1, 1),
            bold=True,
            font_size='14sp'
        )
        info_layout.add_widget(nombre_label)
        
        precio_text = f"{tatuaje['precio_cup']} CUP"
        if tatuaje['tiene_descuento']:
            precio_text = f"OFERTA: {tatuaje['precio_descuento']} CUP"
        
        precio_label = Label(
            text=precio_text,
            size_hint_y=0.5,
            color=(0.2, 0.6, 0.2, 1) if tatuaje['tiene_descuento'] else (0.1, 0.1, 0.1, 1),
            font_size='12sp'
        )
        info_layout.add_widget(precio_label)
        card.add_widget(info_layout)
        
        btn_editar = MDRaisedButton(
            text='Editar',
            size_hint_x=0.2,
            md_bg_color=(0.2, 0.5, 0.8, 1),
            font_size='11sp'
        )
        btn_editar.bind(on_release=lambda x: self.mostrar_popup_editar_tatuaje(tatuaje))
        
        btn_eliminar = MDRaisedButton(
            text='Eliminar',
            size_hint_x=0.2,
            md_bg_color=(0.8, 0.2, 0.2, 1),
            font_size='11sp'
        )
        btn_eliminar.bind(on_release=lambda x: self.eliminar_tatuaje(tatuaje))
        
        card.add_widget(btn_editar)
        card.add_widget(btn_eliminar)
        
        grid.add_widget(card)
    
    def cargar_categorias(self):
        try:
            response = supabase.table("categorias").select("*").execute()
            self.categorias_data = response.data
        except Exception as e:
            print("Error cargando categorías:", e)
    
    def mostrar_popup_anadir_tatuaje(self):
        content = BoxLayout(orientation='vertical', padding="20dp", spacing="15dp")
        
        content.add_widget(Label(
            text='AGREGAR NUEVO TATUAJE', 
            bold=True, 
            size_hint_y=None, 
            height="40dp",
            font_size='18sp'
        ))
        
        nombre_input = TextInput(
            hint_text='Nombre del tatuaje', 
            size_hint_y=None, 
            height="45dp",
            background_color=(1, 1, 1, 0.9)
        )
        descripcion_input = TextInput(
            hint_text='Descripcion', 
            size_hint_y=None, 
            height="70dp",
            background_color=(1, 1, 1, 0.9)
        )
        precio_input = TextInput(
            hint_text='Precio en CUP', 
            size_hint_y=None, 
            height="45dp",
            background_color=(1, 1, 1, 0.9)
        )
        url_input = TextInput(
            hint_text='URL de la imagen', 
            size_hint_y=None, 
            height="45dp",
            background_color=(1, 1, 1, 0.9)
        )
        
        spinner_categoria = Spinner(
            text='Seleccionar categoria', 
            size_hint_y=None, 
            height="45dp"
        )
        
        descuento_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height="45dp",
            spacing="10dp"
        )
        descuento_layout.add_widget(Label(text='Incluir descuento?'))
        switch_descuento = Switch(active=False, size_hint_x=0.3)
        descuento_layout.add_widget(switch_descuento)
        
        precio_descuento_input = TextInput(
            hint_text='Precio con descuento',
            size_hint_y=None,
            height="45dp",
            disabled=True,
            background_color=(0.9, 0.9, 0.9, 0.7)
        )
        
        def on_descuento_switch(instance, value):
            precio_descuento_input.disabled = not value
            precio_descuento_input.background_color = (1, 1, 1, 0.9) if value else (0.9, 0.9, 0.9, 0.7)
        
        switch_descuento.bind(active=on_descuento_switch)
        
        botones_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height="50dp",
            spacing="20dp"
        )
        btn_guardar = MDRaisedButton(text='Guardar')
        btn_cancelar = MDRaisedButton(text='Cancelar')
        botones_layout.add_widget(btn_guardar)
        botones_layout.add_widget(btn_cancelar)
        
        content.add_widget(nombre_input)
        content.add_widget(descripcion_input)
        content.add_widget(precio_input)
        content.add_widget(url_input)
        content.add_widget(spinner_categoria)
        content.add_widget(descuento_layout)
        content.add_widget(precio_descuento_input)
        content.add_widget(botones_layout)
        
        popup = Popup(
            title='', 
            content=content, 
            size_hint=(0.85, 0.9),
            background=''
        )
        
        try:
            response = supabase.table("categorias").select("*").execute()
            categorias = response.data
            spinner_categoria.values = [cat['nombre'] for cat in categorias]
        except Exception as e:
            print("Error cargando categorías:", e)
        
        def guardar_tatuaje(instance):
            categoria_id = None
            for cat in categorias:
                if cat['nombre'] == spinner_categoria.text:
                    categoria_id = cat['id']
                    break
            
            nuevo_tatuaje = {
                'nombre_estilo': nombre_input.text,
                'descripcion': descripcion_input.text,
                'precio_cup': float(precio_input.text) if precio_input.text else 0,
                'url_imagen': url_input.text,
                'categoria_id': categoria_id,
                'tiene_descuento': switch_descuento.active,
                'precio_descuento': float(precio_descuento_input.text) if precio_descuento_input.text and switch_descuento.active else None
            }
            
            try:
                supabase.table("catalogos").insert(nuevo_tatuaje).execute()
                popup.dismiss()
                self.cargar_tatuajes_admin()
            except Exception as e:
                print("Error guardando tatuaje:", e)
        
        btn_guardar.bind(on_release=guardar_tatuaje)
        btn_cancelar.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def mostrar_popup_editar_tatuaje(self, tatuaje):
        # Similar estructura al de añadir pero precargando datos
        content = BoxLayout(orientation='vertical', padding="20dp", spacing="15dp")
        
        content.add_widget(Label(
            text='EDITAR TATUAJE', 
            bold=True, 
            size_hint_y=None, 
            height="40dp",
            font_size='18sp'
        ))
        
        nombre_input = TextInput(
            text=tatuaje['nombre_estilo'], 
            size_hint_y=None, 
            height="45dp"
        )
        descripcion_input = TextInput(
            text=tatuaje['descripcion'] or '', 
            size_hint_y=None, 
            height="70dp"
        )
        precio_input = TextInput(
            text=str(tatuaje['precio_cup']), 
            size_hint_y=None, 
            height="45dp"
        )
        url_input = TextInput(
            text=tatuaje['url_imagen'], 
            size_hint_y=None, 
            height="45dp"
        )
        
        spinner_categoria = Spinner(
            text='Seleccionar categoria', 
            size_hint_y=None, 
            height="45dp"
        )
        
        descuento_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height="45dp",
            spacing="10dp"
        )
        descuento_layout.add_widget(Label(text='Incluir descuento?'))
        switch_descuento = Switch(active=tatuaje['tiene_descuento'])
        descuento_layout.add_widget(switch_descuento)
        
        precio_descuento_input = TextInput(
            text=str(tatuaje['precio_descuento']) if tatuaje['precio_descuento'] else '',
            hint_text='Precio con descuento',
            size_hint_y=None,
            height="45dp",
            disabled=not tatuaje['tiene_descuento']
        )
        
        def on_descuento_switch(instance, value):
            precio_descuento_input.disabled = not value
        
        switch_descuento.bind(active=on_descuento_switch)
        
        botones_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height="50dp",
            spacing="20dp"
        )
        btn_guardar = MDRaisedButton(text='Guardar Cambios')
        btn_cancelar = MDRaisedButton(text='Cancelar')
        botones_layout.add_widget(btn_guardar)
        botones_layout.add_widget(btn_cancelar)
        
        content.add_widget(nombre_input)
        content.add_widget(descripcion_input)
        content.add_widget(precio_input)
        content.add_widget(url_input)
        content.add_widget(spinner_categoria)
        content.add_widget(descuento_layout)
        content.add_widget(precio_descuento_input)
        content.add_widget(botones_layout)
        
        popup = Popup(title='', content=content, size_hint=(0.85, 0.9))
        
        try:
            response = supabase.table("categorias").select("*").execute()
            categorias = response.data
            spinner_categoria.values = [cat['nombre'] for cat in categorias]
            for cat in categorias:
                if cat['id'] == tatuaje['categoria_id']:
                    spinner_categoria.text = cat['nombre']
                    break
        except Exception as e:
            print("Error cargando categorías:", e)
        
        def guardar_cambios(instance):
            categoria_id = None
            for cat in categorias:
                if cat['nombre'] == spinner_categoria.text:
                    categoria_id = cat['id']
                    break
            
            tatuaje_actualizado = {
                'nombre_estilo': nombre_input.text,
                'descripcion': descripcion_input.text,
                'precio_cup': float(precio_input.text) if precio_input.text else 0,
                'url_imagen': url_input.text,
                'categoria_id': categoria_id,
                'tiene_descuento': switch_descuento.active,
                'precio_descuento': float(precio_descuento_input.text) if precio_descuento_input.text and switch_descuento.active else None
            }
            
            try:
                supabase.table("catalogos").update(tatuaje_actualizado).eq('id', tatuaje['id']).execute()
                popup.dismiss()
                self.cargar_tatuajes_admin()
            except Exception as e:
                print("Error actualizando tatuaje:", e)
        
        btn_guardar.bind(on_release=guardar_cambios)
        btn_cancelar.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def eliminar_tatuaje(self, tatuaje):
        content = BoxLayout(orientation='vertical', padding="20dp", spacing="15dp")
        content.add_widget(Label(
            text=f'¿Eliminar "{tatuaje["nombre_estilo"]}"?',
            size_hint_y=None,
            height="40dp",
            font_size='16sp'
        ))
        
        btn_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height="50dp",
            spacing="20dp"
        )
        btn_si = MDRaisedButton(
            text='Si, eliminar', 
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        btn_no = MDRaisedButton(text='Cancelar')
        btn_layout.add_widget(btn_si)
        btn_layout.add_widget(btn_no)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Confirmar eliminacion', 
            content=content, 
            size_hint=(0.6, 0.3)
        )
        
        def confirmar_eliminacion(instance):
            try:
                supabase.table("catalogos").delete().eq('id', tatuaje['id']).execute()
                popup.dismiss()
                self.cargar_tatuajes_admin()
            except Exception as e:
                print("Error eliminando tatuaje:", e)
        
        btn_si.bind(on_release=confirmar_eliminacion)
        btn_no.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def mostrar_popup_gestion_categorias(self):
        content = BoxLayout(orientation='vertical', padding="20dp", spacing="15dp")
        
        content.add_widget(Label(
            text='GESTIONAR CATEGORIAS', 
            bold=True,
            size_hint_y=None,
            height="40dp",
            font_size='18sp'
        ))
        
        scroll = ScrollView(size_hint_y=0.6)
        categorias_layout = GridLayout(cols=1, spacing="10dp", size_hint_y=None)
        categorias_layout.bind(minimum_height=categorias_layout.setter('height'))
        
        try:
            response = supabase.table("categorias").select("*").execute()
            categorias = response.data
            
            for categoria in categorias:
                cat_box = BoxLayout(
                    orientation='horizontal', 
                    size_hint_y=None, 
                    height="50dp",
                    spacing="10dp"
                )
                cat_box.add_widget(Label(
                    text=categoria['nombre'], 
                    size_hint_x=0.4,
                    bold=True
                ))
                cat_box.add_widget(Label(
                    text=categoria['descripcion'], 
                    size_hint_x=0.4
                ))
                
                btn_eliminar = MDRaisedButton(
                    text='Eliminar', 
                    size_hint_x=0.2,
                    md_bg_color=(0.8, 0.2, 0.2, 1)
                )
                btn_eliminar.bind(on_release=lambda x, cat=categoria: self.eliminar_categoria(cat))
                cat_box.add_widget(btn_eliminar)
                
                categorias_layout.add_widget(cat_box)
        except Exception as e:
            print("Error:", e)
        
        scroll.add_widget(categorias_layout)
        
        form_layout = BoxLayout(
            orientation='vertical', 
            size_hint_y=0.4, 
            spacing="10dp"
        )
        nuevo_nombre = TextInput(
            hint_text='Nombre categoria', 
            size_hint_y=None, 
            height="45dp"
        )
        nueva_desc = TextInput(
            hint_text='Descripcion', 
            size_hint_y=None, 
            height="60dp"
        )
        
        btn_anadir = MDRaisedButton(
            text='Agregar Categoria', 
            size_hint_y=None, 
            height="45dp"
        )
        btn_cerrar = MDRaisedButton(
            text='Cerrar', 
            size_hint_y=None, 
            height="45dp"
        )
        
        def anadir_categoria(instance):
            if nuevo_nombre.text:
                supabase.table("categorias").insert({
                    'nombre': nuevo_nombre.text,
                    'descripcion': nueva_desc.text
                }).execute()
                popup.dismiss()
                self.mostrar_popup_gestion_categorias()
        
        form_layout.add_widget(nuevo_nombre)
        form_layout.add_widget(nueva_desc)
        form_layout.add_widget(btn_anadir)
        form_layout.add_widget(btn_cerrar)
        
        content.add_widget(scroll)
        content.add_widget(form_layout)
        
        popup = Popup(title='', content=content, size_hint=(0.8, 0.8))
        
        btn_anadir.bind(on_release=anadir_categoria)
        btn_cerrar.bind(on_release=popup.dismiss)
        
        popup.open()
    
    def eliminar_categoria(self, categoria):
        try:
            supabase.table("categorias").delete().eq('id', categoria['id']).execute()
            self.mostrar_popup_gestion_categorias()
        except Exception as e:
            print("Error eliminando categoria:", e)

class AboutScreen(Screen):
    def abrir_whatsapp_soporte(self):
        numero = "+5359086563"
        mensaje = "Hola! Necesito soporte con la app del catalogo de tatuajes."
        url_whatsapp = f"https://wa.me/{numero}?text={mensaje}"
        webbrowser.open(url_whatsapp)

class MenuScreen(Screen):
    pass

class CatalogoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.theme_style = "Light"
        self.title = "AzojuanitoP41 - Catálogo de Tatuajes"
        
        # 🎯 CONFIGURACIÓN DEL ICONO
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(base_path, 'iconoTattoo.ico')
        if os.path.exists(icon_path):
            Window.set_icon(icon_path)
            self.icon = icon_path
        
        # 🎯 CARGA SEGURA DEL ARCHIVO KV
        try:
            # Intenta cargar desde el directorio del ejecutable
            kv_path = os.path.join(base_path, 'catalogo.kv')
            if os.path.exists(kv_path):
                Builder.load_file(kv_path)
            else:
                # Si no se encuentra, intenta cargar directamente
                Builder.load_file('catalogo.kv')
        except Exception as e:
            print(f"Error cargando archivo KV: {e}")
            # Si falla, muestra un mensaje de error
            from kivy.uix.label import Label
            return Label(text=f'Error cargando interfaz: {e}', font_size='20sp')
        
        # 🎯 CONSTRUIR EL SCREEN MANAGER - ESTO ES LO QUE FALTABA
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CatalogoScreen(name='catalogo'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(AboutScreen(name='about'))
        
        return sm  # ⚠️ IMPORTANTE: Retornar el ScreenManager

if __name__ == '__main__':
    CatalogoApp().run()