import objc
import AppKit
import Foundation
import os
import subprocess


NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
NSURL = objc.lookUpClass('NSURL')
NSImage = objc.lookUpClass('NSImage')


def notify(title, subtitle=None, info_text=None, identity_image=None, content_image=None, delay=0, sound=False):
  notification = NSUserNotification.alloc().init()
  notification.setTitle_(title)

  if subtitle:
    notification.setSubtitle_(subtitle)

  if info_text:
    notification.setInformativeText_(info_text)

  # identity_image is the image on the left side
  # this does NOT override the app image (defaults to the Python Rocket)
  # if you build the app with py2app, the default identity_image is your app's icon

  # note that unless you build an app, you cannot change the Python rocket to something else
  if identity_image:
    identity_image_path = f'file:{os.getcwd()}/{identity_image}'
    url = NSURL.alloc().initWithString_(identity_image_path)
    image = NSImage.alloc().initWithContentsOfURL_(url)
    notification.set_identityImage_(image)

  # content_image is the image on the right side
  if content_image:
    content_image_path = f'file:{os.getcwd()}/{content_image}'
    print(content_image_path)
    url = NSURL.alloc().initWithString_(content_image_path)
    image = NSImage.alloc().initWithContentsOfURL_(url)
    print(image)
    notification.setContentImage_(image)

  if sound:
    notification.setSoundName_('NSUserNotificationDefaultSoundName')

  # pylint: disable=no-member
  notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))

  try:
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
  except:
    as_notify(title=title, subtitle=subtitle, info_text=info_text)


def as_notify(title, subtitle=None, info_text=None):
  applescript = 'display notification'
  if info_text:
    # applescript = f'''\
    # display notification with title "{title}" \
    # '''
    applescript += f' "{info_text}"'
  
  applescript += f' with title "{title}"'

  if subtitle is not None:
    applescript += f' subtitle "{subtitle}"'

  command = f'osascript -e \'{applescript}\''
  subprocess.check_output(command, shell=True)