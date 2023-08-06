"""
Webstaterator

A Python tool for generating static websites based on object models

Documentation: TBA
Gitlab: https://gitlab.com/Jon.Keatley.Folio/webstaterator
PyPi: Some day!

Created by Jon Keatley (http://jon-keatley.com)
Named by Sasha Siegel. It is her fault!

Copyright Jon Keatley 2020

"""

import sys
import os
import shutil

from webstaterator.website import Website, PageAttributes
from webstaterator.templateengine import TemplateEngine

class Webstaterator:
    """ A Python tool for generating static websites based on object models """

    def validate(self, website_model):
        """ Validates a websites settings """
        website = Website()

        try:
            website.load(website_model)
            templates = TemplateEngine(website.template_path)

            #check all templates exist
            pages = website.pages
            missing_page_format = "Template {} for page {} was not found"

            has_error = False
            for page in pages:
                if not templates.has_template(page[PageAttributes.TEMPLATE]):
                    err = missing_page_format.format(
                        page[PageAttributes.TEMPLATE],
                        page[PageAttributes.NAME]
                    )
                    has_error = True
                    print(err)


            website.generate_links()

            if not has_error:
                print("Ok")
        except Exception as ex:
            print("An error was found with your website!")
            print("Error: {}. Message: {}".format(type(ex).__name__,ex.args))


    def build(self, website_model, path):
        """ Builds a website based on the provided settings """

        # add check for path
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)

        print("Loading ...")
        website = Website()
        try:
            website.load(website_model)
            website.generate_links()
            templates = TemplateEngine(website.template_path)
            templates.model = website.model
            templates.links = website.links
        except Exception as ex:
            print("An error was found with your website!")
            print("Error: {}. Message: {}".format(type(ex).__name__,ex.args))
            sys.exit(-1)

        links = website.links

        if website.asset_paths is not None:
            print("copying assets")
            for asset in website.asset_paths:
                if os.path.isdir(asset):
                    dir_name = os.path.basename(asset)
                    new_asset_path = os.path.join(path,dir_name)

                    shutil.copytree(
                        asset,
                        new_asset_path
                    )
                else:
                    print("Asset path {} does not exist".format(website.asset_path))
                    sys.exit(-1)


        print("Building website")
        for page in website.pages:
            page_links = links[page[PageAttributes.NAME]]

            for page_link in page_links:
                save_path = os.path.join(path,page_link)
                templates.generate_page(
                    page[PageAttributes.TEMPLATE],
                    save_path,
                    page_link,
                    target = website.get_target(page_link)
                )

        print("Built!")


    def template(self, name= None):
        """ Generates a template for a website """
        raise NotImplementedError
